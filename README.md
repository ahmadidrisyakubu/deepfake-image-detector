# Deepfake Image Detector

A Flask-based web application that detects whether an image is **Real** or **Fake** (AI-generated/artificial) using a fine-tuned SigLIP model from Hugging Face.

## Features

- **AI-Powered Detection**: Uses the `waleeyd/deepfake-detector` model from Hugging Face
- **Modified Classification Logic**: 
  - "Deepfake" + "Real" → **Real**
  - "Artificial" → **Fake**
- **Modern UI**: Beautiful, responsive interface with glassmorphism effects
- **Security Features**: Rate limiting, file validation, CSRF protection, and security headers
- **Railway-Ready**: Configured for easy deployment on Railway

## Classification Logic

The original model classifies images into three categories:
- **Artificial** (AI-generated)
- **Deepfake** (Face-swapped/manipulated)
- **Real** (Authentic)

Our modified logic simplifies this to:
- **Fake**: Images classified as "Artificial"
- **Real**: Images classified as "Deepfake" or "Real"

## Tech Stack

- **Backend**: Flask, PyTorch, Transformers
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Model**: SigLIP-based classifier from Hugging Face
- **Deployment**: Railway (or any Python hosting platform)

## Local Development

### Prerequisites

- Python 3.11+
- pip

### Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd deepfake-detector
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python app.py
```

5. Open your browser and navigate to:
```
http://localhost:5000
```

## Deployment on Railway

### Method 1: Deploy from GitHub

1. **Push your code to GitHub**:
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```

2. **Deploy on Railway**:
   - Go to [Railway.app](https://railway.app)
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository
   - Railway will automatically detect the configuration

3. **Wait for deployment**:
   - Railway will install dependencies (this may take 5-10 minutes due to PyTorch)
   - The model will be downloaded from Hugging Face on first run
   - Once deployed, Railway will provide a public URL

### Method 2: Deploy with Railway CLI

1. **Install Railway CLI**:
```bash
npm install -g @railway/cli
```

2. **Login to Railway**:
```bash
railway login
```

3. **Initialize and deploy**:
```bash
railway init
railway up
```

### Important Notes for Railway

- **Memory Requirements**: The app requires at least **2GB RAM** due to the PyTorch model
- **First Load Time**: The first request will take longer as the model downloads from Hugging Face (~500MB)
- **Environment Variables**: No additional environment variables are required
- **Port Configuration**: The app automatically uses the `PORT` environment variable provided by Railway

## Project Structure

```
deepfake-detector/
├── app.py                 # Flask application with model logic
├── requirements.txt       # Python dependencies
├── Procfile              # Railway/Heroku deployment config
├── runtime.txt           # Python version specification
├── .gitignore            # Git ignore rules
├── README.md             # This file
├── templates/
│   └── index.html        # Frontend UI
├── static/               # Static assets (if needed)
└── uploads/              # Temporary upload directory
    └── .gitkeep
```

## API Endpoint

### POST /predict

Upload an image for deepfake detection.

**Request**:
- Method: `POST`
- Content-Type: `multipart/form-data`
- Body: `image` (file)

**Response**:
```json
{
  "label": "Real",
  "confidence": 87.45,
  "hash": "abc123..."
}
```

**Error Response**:
```json
{
  "error": "Error message"
}
```

## Security Features

- **Rate Limiting**: 100 requests/hour, 20 requests/minute per IP
- **File Validation**: Only PNG, JPG, JPEG files up to 30MB
- **Image Verification**: Validates image integrity before processing
- **Security Headers**: HSTS, X-Frame-Options, CSP, etc.
- **File Sanitization**: Secure filename handling
- **Automatic Cleanup**: Uploaded files are deleted after processing

## Model Information

- **Model**: [waleeyd/deepfake-detector](https://huggingface.co/waleeyd/deepfake-detector)
- **Base Architecture**: SigLIP (Sigmoid Loss for Language-Image Pre-training)
- **Input Size**: 224x224 pixels
- **Normalization**: Mean=[0.5, 0.5, 0.5], Std=[0.5, 0.5, 0.5]

## Troubleshooting

### Model Download Issues
If the model fails to download, ensure you have a stable internet connection. The model is approximately 500MB.

### Memory Issues on Railway
If you encounter memory errors, upgrade to a Railway plan with more RAM (at least 2GB recommended).

### Slow First Request
The first request after deployment will be slow as the model loads into memory. Subsequent requests will be much faster.

## License

This project is open source and available under the MIT License.

## Credits

- Model: [waleeyd/deepfake-detector](https://huggingface.co/waleeyd/deepfake-detector)
- UI Design: Custom glassmorphism design
- Framework: Flask, PyTorch, Transformers

## Support

For issues or questions, please open an issue on GitHub.
