import os
import time
import hashlib
import logging
import secrets
from functools import wraps

from flask import Flask, request, render_template, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_limiter.errors import RateLimitExceeded
from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm
from wtforms import FileField
from wtforms.validators import DataRequired
from werkzeug.utils import secure_filename
from PIL import Image
import torch
import torchvision.transforms as T
import numpy as np

# ========== CONFIG ==========
MODEL_NAME = os.environ.get("MODEL_NAME", "waleeyd/deepfake-detector")
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
MAX_FILE_SIZE = 30 * 1024 * 1024  # 30MB

# ========== APP SETUP ==========
app = Flask(__name__, static_folder="static", template_folder="templates")
app.config.update(
    SECRET_KEY=os.environ.get("SECRET_KEY", secrets.token_hex(32)),
    MAX_CONTENT_LENGTH=MAX_FILE_SIZE,
    WTF_CSRF_TIME_LIMIT=None,
    UPLOAD_FOLDER=UPLOAD_FOLDER,
)

csrf = CSRFProtect(app)

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["100 per hour", "20 per minute"]
)
limiter.init_app(app)

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# ========== LOGGING ==========
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("security.log"), logging.StreamHandler()]
)

# ========== DEVICE & MODEL LOADING ==========
device = "cuda" if torch.cuda.is_available() else "cpu"
logging.info(f"Using device: {device}")

try:
    from transformers import SiglipForImageClassification
    # Load model (will download from HF if not present)
    model = SiglipForImageClassification.from_pretrained(
        MODEL_NAME,
        torch_dtype=torch.float32,
        local_files_only=False
    ).to(device)
    model.eval()
    logging.info(f"Model {MODEL_NAME} loaded successfully")
except Exception as e:
    logging.error(f"Failed to load model {MODEL_NAME}: {e}")
    model = None

# ========== IMAGE PREPROCESS ==========
transform = T.Compose([
    T.Resize((224, 224)),
    T.ToTensor(),
    T.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
])

# ========== HELPERS ==========
class UploadForm(FlaskForm):
    image = FileField("Image", validators=[DataRequired()])

def security_validate(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        logging.info(f"{request.remote_addr} → {request.endpoint}")
        return f(*args, **kwargs)
    return wrapper

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def sanitize_filename(filename):
    name, ext = os.path.splitext(secure_filename(filename))
    return f"{name}_{int(time.time())}{ext}"

def validate_file_security(file_obj):
    if not file_obj or file_obj.filename == "":
        return ["No file provided"]

    file_obj.seek(0, os.SEEK_END)
    size = file_obj.tell()
    file_obj.seek(0)

    errors = []
    if size > MAX_FILE_SIZE:
        errors.append("File exceeds 30MB limit")
    if not allowed_file(file_obj.filename):
        errors.append("Invalid file extension")

    try:
        img = Image.open(file_obj)
        img.verify()
    except Exception:
        errors.append("Invalid or corrupted image file")
    finally:
        file_obj.seek(0)

    return errors

def generate_file_hash(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return h.hexdigest()

def predict_image_with_model(path):
    """
    Runs the HF Siglip model and converts its three-class output into:
      - 'Fake'  if predicted class = Artificial (id 0)
      - 'Real'  if predicted class = Deepfake (id 1) OR Real (id 2)
    Confidence is computed as:
      - fake_conf = prob(class0)
      - real_conf = prob(class1) + prob(class2)
    Returns (label, confidence_percent, raw_scores_dict)
    """
    if model is None:
        raise RuntimeError("Model not loaded")

    img = Image.open(path).convert("RGB")
    tensor = transform(img).unsqueeze(0).to(device)

    with torch.no_grad():
        outputs = model(pixel_values=tensor)
        probs = torch.softmax(outputs.logits, dim=1).squeeze().cpu().numpy()

    # probs order assumed: [Artificial, Deepfake, Real]
    artificial_p, deepfake_p, real_p = float(probs[0]), float(probs[1]), float(probs[2])

    fake_conf = artificial_p
    real_conf = deepfake_p + real_p

    if real_conf >= fake_conf:
        label = "Real"
        confidence = round(real_conf * 100, 2)
    else:
        label = "Fake"
        confidence = round(fake_conf * 100, 2)

    raw_scores = {
        "Artificial": round(artificial_p * 100, 4),
        "Deepfake": round(deepfake_p * 100, 4),
        "Real": round(real_p * 100, 4),
    }

    return label, confidence, raw_scores

# ========== ROUTES ==========
@app.route("/", methods=["GET"])
@limiter.limit("30 per minute")
@security_validate
def index():
    return render_template("index.html", form=UploadForm())

@app.route("/predict", methods=["POST"])
@csrf.exempt
@limiter.limit("60 per minute")
@security_validate
def predict():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files["image"]
    errors = validate_file_security(file)
    if errors:
        return jsonify({"error": "; ".join(errors)}), 400

    filename = sanitize_filename(file.filename)
    path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    try:
        img = Image.open(file).convert("RGB")
        img.thumbnail((2048, 2048))
        img.save(path, "JPEG", quality=95)

        label, confidence, raw_scores = predict_image_with_model(path)
        file_hash = generate_file_hash(path)

        return jsonify({
            "label": label,
            "confidence": confidence,
            "hash": file_hash,
            "raw_scores": raw_scores
        })

    except Exception as e:
        logging.error(f"Prediction failed: {e}")
        return jsonify({"error": "Prediction failed"}), 500

    finally:
        if os.path.exists(path):
            try:
                os.remove(path)
            except Exception:
                pass

# ========== SECURITY HEADERS ==========
@app.after_request
def security_headers(res):
    res.headers["X-Content-Type-Options"] = "nosniff"
    res.headers["X-Frame-Options"] = "DENY"
    res.headers["X-XSS-Protection"] = "1; mode=block"
    res.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    res.headers["Content-Security-Policy"] = (
        "default-src 'self' https://cdnjs.cloudflare.com; "
        "style-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com https://fonts.googleapis.com; "
        "script-src 'self' 'unsafe-inline'; "
        "img-src 'self' data: https:; "
        "font-src 'self' https://fonts.gstatic.com https://cdnjs.cloudflare.com; "
        "frame-src https://www.youtube.com https://www.youtube-nocookie.com;"
    )
    return res

# ========== ERROR HANDLERS ==========
@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({"error": "File too large. Maximum allowed size is 30 MB."}), 413

@app.errorhandler(RateLimitExceeded)
def rate_limit_handler(e):
    return jsonify({"error": "Too many requests. Please slow down."}), 429

@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": "Invalid request or image file."}), 400

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error during prediction."}), 500

# ========== START ==========
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
