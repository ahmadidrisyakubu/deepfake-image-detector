# Deepfake Detection Tool

A Flask-based web application for detecting AI-generated, deepfake, and real images using PyTorch and Transformers.

## Features

- **AI-Powered Detection**: Uses the `waleeyd/deepfake-detector` model from Hugging Face
- **Custom Label Mapping**: 
  - Artificial → Fake
  - Deepfake/Real → Real
- **Modern UI**: Beautiful glassmorphism design with animations
- **Security**: Rate limiting, CSRF protection, file validation
- **Railway Ready**: Configured for easy deployment on Railway

## Model Information

- **Model**: SiglipForImageClassification
- **Source**: Hugging Face (`waleeyd/deepfake-detector`)
- **Classes**: Artificial, Deepfake, Real
- **Input Size**: 224x224 pixels

## Deployment on Railway

### Prerequisites
- A Railway account ([railway.app](https://railway.app))
- Git installed on your machine

### Steps

1. **Initialize Git Repository**
   ```bash
   cd deepfake-detector
   git init
   git add .
   git commit -m "Initial commit"
   ```

2. **Create GitHub Repository**
   - Go to GitHub and create a new repository
   - Push your code:
     ```bash
     git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
     git branch -M main
     git push -u origin main
     ```

3. **Deploy on Railway**
   - Go to [railway.app](https://railway.app)
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository
   - Railway will automatically detect the configuration and deploy

4. **Environment Variables** (Optional)
   - No additional environment variables required
   - Railway will automatically set `PORT`

5. **Access Your App**
   - Railway will provide a public URL
   - Click on the URL to access your deployed app

## Local Development

### Installation

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running Locally

```bash
python app.py
```

The app will be available at `http://localhost:5000`

## File Structure

```
deepfake-detector/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── Procfile              # Railway/Heroku process configuration
├── runtime.txt           # Python version specification
├── .gitignore            # Git ignore rules
├── README.md             # This file
├── templates/
│   └── index.html        # Main HTML template
├── static/               # Static files (CSS, JS, images)
└── uploads/              # Temporary upload directory (auto-created)
```

## Configuration

### Maximum File Size
- Default: 30 MB
- Change in `app.py`: `MAX_CONTENT_LENGTH = 30 * 1024 * 1024`

### Rate Limiting
- Default: 100 requests/hour, 20 requests/minute
- Change in `app.py`: `default_limits=["100 per hour", "20 per minute"]`

### Allowed File Types
- Supported: PNG, JPG, JPEG
- Change in `app.py`: `ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}`

## Security Features

- CSRF Protection
- Rate Limiting
- File Type Validation
- File Size Limits
- Security Headers (CSP, X-Frame-Options, etc.)
- Image Verification
- SHA256 File Hashing

## Model Download

The model is automatically downloaded from Hugging Face on first run. This may take a few minutes depending on your internet connection. The model size is approximately 400-500 MB.

## Troubleshooting

### Model Loading Issues
- Ensure you have a stable internet connection for the initial model download
- Check Railway logs for any error messages
- The model requires approximately 1-2 GB of RAM

### Memory Issues on Railway
- Railway's free tier has memory limits
- Consider upgrading to a paid plan for better performance
- Reduce the number of workers in `Procfile` if needed

### Slow Predictions
- First prediction may be slower due to model initialization
- Consider using GPU instances for faster inference (paid plans)

## License

This project is open source and available under the MIT License.

## Credits

- Model: [waleeyd/deepfake-detector](https://huggingface.co/waleeyd/deepfake-detector)
- Framework: Flask, PyTorch, Transformers
- UI Design: Custom glassmorphism design

## Support

For issues or questions, please open an issue on the GitHub repository.
