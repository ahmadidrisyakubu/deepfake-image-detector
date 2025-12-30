# Project Summary: Deepfake Detection Tool for Railway

## Overview

This project is a Flask-based web application that detects whether an image is AI-generated (fake) or real using a PyTorch deep learning model from Hugging Face.

## Key Modifications from Original Requirements

### 1. **Label Mapping** ✅
As requested, the label mapping has been customized:
- **Artificial** → **Fake**
- **Deepfake** → **Real**
- **Real** → **Real**

This is implemented in the `predict_image()` function in `app.py`:
```python
# Map labels: Artificial -> Fake, Deepfake/Real -> Real
if max_class == "Artificial":
    label = "Fake"
    confidence = max_prob
else:  # Deepfake or Real
    label = "Real"
    # Combine probabilities for Deepfake and Real
    confidence = predictions["Deepfake"] + predictions["Real"]
```

### 2. **Model Integration** ✅
- Uses the **waleeyd/deepfake-detector** model from Hugging Face
- PyTorch + Transformers (SiglipForImageClassification)
- Model is automatically downloaded on first run
- No need to upload the model manually - it's fetched from Hugging Face

### 3. **UI Design** ✅
- Copied the complete UI template from your provided Flask app
- Beautiful glassmorphism design with animations
- Responsive layout with tabbed navigation
- Modern dark theme with gradient effects
- All CSS and JavaScript included in `templates/index.html`

### 4. **Railway Deployment** ✅
Configured for seamless Railway deployment:
- `Procfile`: Gunicorn configuration
- `requirements.txt`: All Python dependencies
- `runtime.txt`: Python version specification
- `railway.json`: Railway-specific configuration
- `.gitignore`: Excludes unnecessary files

## File Structure

```
deepfake-detector/
├── app.py                    # Main Flask application with PyTorch model
├── requirements.txt          # Python dependencies
├── Procfile                  # Railway/Heroku deployment config
├── runtime.txt               # Python 3.11.0
├── railway.json              # Railway configuration
├── .gitignore                # Git ignore rules
├── README.md                 # Project documentation
├── DEPLOYMENT_GUIDE.md       # Step-by-step Railway deployment
├── PROJECT_SUMMARY.md        # This file
├── templates/
│   └── index.html           # Complete UI template (your design)
├── static/
│   └── .gitkeep             # Placeholder for static files
└── uploads/
    └── .gitkeep             # Placeholder for temporary uploads
```

## Technical Stack

### Backend
- **Flask 3.0.0**: Web framework
- **PyTorch 2.1.2**: Deep learning framework
- **Transformers 4.36.2**: Hugging Face model library
- **Gunicorn 21.2.0**: Production WSGI server

### Security
- **Flask-Limiter**: Rate limiting (100/hour, 20/minute)
- **Flask-WTF**: CSRF protection
- **PIL/Pillow**: Image validation and processing
- **Security Headers**: CSP, X-Frame-Options, etc.

### Model
- **Name**: waleeyd/deepfake-detector
- **Type**: SiglipForImageClassification
- **Input**: 224x224 RGB images
- **Output**: 3 classes (Artificial, Deepfake, Real)
- **Size**: ~400-500 MB

## Key Features

### 1. **Automatic Model Download**
- Model is downloaded from Hugging Face on first run
- No manual upload required
- Cached for subsequent runs

### 2. **Custom Label Logic**
- Artificial images → Labeled as "Fake"
- Deepfake + Real images → Labeled as "Real"
- Confidence scores properly calculated

### 3. **Security Features**
- File type validation (PNG, JPG, JPEG only)
- File size limit (30 MB max)
- Image verification using PIL
- SHA256 file hashing
- Rate limiting
- CSRF protection
- Security headers

### 4. **Production Ready**
- Gunicorn WSGI server
- 2 workers (configurable)
- 120-second timeout
- Error handling
- Logging to file and console

## Deployment Instructions

### Quick Start

1. **Push to GitHub**:
   ```bash
   cd deepfake-detector
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
   git push -u origin main
   ```

2. **Deploy on Railway**:
   - Go to [railway.app](https://railway.app)
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Wait for deployment (5-10 minutes for first time)

3. **Generate Domain**:
   - In Railway project settings
   - Click "Generate Domain"
   - Access your app via the provided URL

### Detailed Guide
See `DEPLOYMENT_GUIDE.md` for comprehensive step-by-step instructions.

## Configuration Options

### Change File Size Limit
In `app.py`, line 26:
```python
MAX_CONTENT_LENGTH=30 * 1024 * 1024,  # 30 MB
```

### Change Rate Limits
In `app.py`, line 33:
```python
default_limits=["100 per hour", "20 per minute"]
```

### Change Allowed File Types
In `app.py`, line 78:
```python
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
```

### Adjust Workers
In `Procfile`:
```
web: gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120
```

## Testing Locally

1. **Create virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app**:
   ```bash
   python app.py
   ```

4. **Access**:
   - Open browser to `http://localhost:5000`

## Important Notes

### First Deployment
- Takes 5-10 minutes due to model download
- Model size: ~400-500 MB
- Requires stable internet connection

### Memory Requirements
- Minimum: 1-2 GB RAM
- Railway free tier is sufficient for testing
- Consider paid plan for production

### Model Behavior
- **Artificial** images are classified as **Fake**
- **Deepfake** and **Real** images are both classified as **Real**
- This matches your exact requirements

## Differences from Original Gradio App

| Feature | Original (Gradio) | New (Flask) |
|---------|------------------|-------------|
| Framework | Gradio | Flask |
| UI | Gradio default | Custom glassmorphism design |
| Port | 7860 | 5000 (or Railway's PORT) |
| Deployment | Hugging Face Spaces | Railway |
| Labels | 3 classes | 2 classes (Fake/Real) |
| Security | Basic | Enhanced (rate limiting, CSRF, etc.) |
| Production Server | Gradio built-in | Gunicorn |

## What You Need to Do

1. **Download the ZIP file** (`deepfake-detector.zip`)
2. **Extract it** to your local machine
3. **Push to GitHub** (see instructions above)
4. **Deploy on Railway** (see DEPLOYMENT_GUIDE.md)
5. **Wait for model download** (first deployment only)
6. **Test your app** with sample images

## Support

- Check `README.md` for general information
- Check `DEPLOYMENT_GUIDE.md` for deployment help
- Review Railway logs for troubleshooting
- Model documentation: https://huggingface.co/waleeyd/deepfake-detector

---

**Everything is configured and ready to deploy! 🚀**

The model will be automatically downloaded from Hugging Face, so you don't need to upload it manually. Just push to GitHub and deploy on Railway!
