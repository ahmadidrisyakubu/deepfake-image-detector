from flask import Flask, request, render_template, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_limiter.errors import RateLimitExceeded
from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm
from wtforms import FileField
from wtforms.validators import DataRequired
from werkzeug.utils import secure_filename
from functools import wraps
from PIL import Image
import torch
import torchvision.transforms as T
from transformers import AutoModelForImageClassification
import os
import time
import hashlib
import logging
import secrets

# ===============================
# App initialization
# ===============================
app = Flask(__name__)

app.config.update(
    SECRET_KEY=secrets.token_hex(32),
    MAX_CONTENT_LENGTH=30 * 1024 * 1024,  # 30 MB
    WTF_CSRF_TIME_LIMIT=None,
    UPLOAD_FOLDER="uploads"
)

csrf = CSRFProtect(app)

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["100 per hour", "20 per minute"]
)
limiter.init_app(app)

# ===============================
# Logging
# ===============================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("security.log"), logging.StreamHandler()]
)

# ===============================
# Load PyTorch Model
# ===============================
# Using a lighter model for Railway Free Tier (512MB RAM limit)
MODEL_NAME = "prithivMLmods/Deep-Fake-Detector-Model"
ID2LABEL = {
    0: "Fake",
    1: "Real"
}

device = "cuda" if torch.cuda.is_available() else "cpu"

try:
    # Use AutoModel for better compatibility with SigLIP architecture
    # Added trust_remote_code and explicit architecture handling
    model = AutoModelForImageClassification.from_pretrained(
        MODEL_NAME,
        torch_dtype=torch.float32,
        trust_remote_code=True,
        low_cpu_mem_usage=True
    ).to(device)
    model.eval()
    logging.info(f"Model loaded successfully on {device}")
except Exception as e:
    logging.error(f"Model load failed: {e}")
    # Final fallback: try loading with specific architecture if AutoModel fails
    try:
        from transformers import SiglipForImageClassification
        model = SiglipForImageClassification.from_pretrained(
            MODEL_NAME,
            torch_dtype=torch.float32
        ).to(device)
        model.eval()
        logging.info(f"Model loaded successfully using SiglipForImageClassification on {device}")
    except Exception as e2:
        logging.error(f"Final model load fallback failed: {e2}")
        model = None

# Image preprocessing
transform = T.Compose([
    T.Resize((224, 224)),
    T.ToTensor(),
    T.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
])

# ===============================
# Constants
# ===============================
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
MAX_FILE_SIZE = 30 * 1024 * 1024

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# ===============================
# Helpers
# ===============================
def security_validate(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        logging.info(f"{request.remote_addr} → {request.endpoint}")
        return f(*args, **kwargs)
    return wrapper

class UploadForm(FlaskForm):
    image = FileField("Image", validators=[DataRequired()])

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def sanitize_filename(filename):
    name, ext = os.path.splitext(secure_filename(filename))
    return f"{name}_{int(time.time())}{ext}"

def validate_file_security(file):
    if not file or file.filename == "":
        return ["No file provided"]

    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0)

    errors = []

    if size > MAX_FILE_SIZE:
        errors.append("File exceeds 30MB limit")

    if not allowed_file(file.filename):
        errors.append("Invalid file extension")

    try:
        img = Image.open(file)
        img.verify()
    except Exception:
        errors.append("Invalid or corrupted image file")
    finally:
        file.seek(0)

    return errors

def generate_file_hash(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return h.hexdigest()

def predict_image(path):
    if not model:
        raise Exception("Model not loaded")

    image = Image.open(path).convert("RGB")
    tensor = transform(image).unsqueeze(0).to(device)

    with torch.no_grad():
        outputs = model(pixel_values=tensor)
        probs = torch.softmax(outputs.logits, dim=1).squeeze()

    # Get predictions for all classes
    # The new model has 2 classes: 0: Fake, 1: Real
    predictions = {ID2LABEL[i]: float(probs[i]) for i in range(len(ID2LABEL))}
    
    # Find the class with highest probability
    label = max(predictions, key=predictions.get)
    confidence = predictions[label]
    
    return label, round(confidence * 100, 2)

# ===============================
# Routes
# ===============================
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

        label, confidence = predict_image(path)
        file_hash = generate_file_hash(path)

        return jsonify({
            "label": label,
            "confidence": confidence,
            "hash": file_hash
        })

    except Exception as e:
        logging.error(f"Prediction failed: {e}")
        return jsonify({"error": "Prediction failed"}), 500

    finally:
        if os.path.exists(path):
            os.remove(path)

# ===============================
# Security headers
# ===============================
@app.after_request
def security_headers(res):
    res.headers["X-Content-Type-Options"] = "nosniff"
    res.headers["X-Frame-Options"] = "DENY"
    res.headers["X-XSS-Protection"] = "1; mode=block"
    res.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    res.headers["Content-Security-Policy"] = (
        "default-src 'self' https://cdnjs.cloudflare.com; "
        "style-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com; "
        "script-src 'self' 'unsafe-inline'; "
        "img-src 'self' data:; "
        "font-src 'self' https://cdnjs.cloudflare.com; "
        "frame-src https://www.youtube.com https://www.youtube-nocookie.com;"
    )
    return res

# ===============================
# JSON Error Handlers
# ===============================
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

# ===============================
# Run
# ===============================
if __name__ == "__main__":
    # Get port from environment variable, default to 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(
        debug=False,
        host="0.0.0.0",
        port=port
    )
