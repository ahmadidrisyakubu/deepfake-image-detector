# Quick Start Guide

Get your Deepfake Detector up and running in minutes!

## 🚀 Deploy to Railway (Recommended)

### Step 1: Push to GitHub
```bash
cd deepfake-detector
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/deepfake-detector.git
git push -u origin main
```

### Step 2: Deploy on Railway
1. Go to [railway.app](https://railway.app)
2. Login with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your `deepfake-detector` repository
5. Wait 10-15 minutes for deployment
6. Get your public URL from Railway dashboard

### Step 3: Test
- Open the Railway URL
- Upload an image
- Click "Analyze Image"
- See results!

**⚠️ Important**: You need Railway's **Developer Plan** ($20/month) for sufficient RAM.

---

## 💻 Run Locally

### Quick Method (Linux/Mac)
```bash
./run_local.sh
```

### Manual Method
```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

Open browser: http://localhost:5000

---

## 📝 Key Files

| File | Purpose |
|------|---------|
| `app.py` | Main Flask application |
| `templates/index.html` | Frontend UI |
| `requirements.txt` | Python dependencies |
| `Procfile` | Railway deployment config |
| `README.md` | Full documentation |
| `DEPLOYMENT_GUIDE.md` | Detailed deployment steps |

---

## ⚙️ How It Works

1. **Upload image** → Frontend validates
2. **Send to backend** → `/predict` endpoint
3. **Model analyzes** → SigLIP classifier
4. **Modified logic** → Artificial=Fake, Deepfake+Real=Real
5. **Display results** → Confidence + label

---

## 🔧 Configuration

### Classification Logic
- **Fake**: AI-generated (Artificial) images
- **Real**: Authentic + Deepfake images

### Security
- Max file size: 30MB
- Allowed formats: PNG, JPG, JPEG
- Rate limit: 20 requests/minute

---

## 📚 Documentation

- **Full docs**: `README.md`
- **Deployment**: `DEPLOYMENT_GUIDE.md`
- **Testing**: `TESTING.md`
- **Summary**: `PROJECT_SUMMARY.md`

---

## ❓ Troubleshooting

**Problem**: Out of memory on Railway
**Solution**: Upgrade to Developer plan (8GB RAM)

**Problem**: Model download fails
**Solution**: Check internet connection, retry

**Problem**: Slow first request
**Solution**: Normal! Model downloads (~500MB) on first run

---

## 📞 Need Help?

1. Check the documentation files
2. Review Railway logs
3. Open a GitHub issue

---

## ✅ Success Checklist

- [ ] Code pushed to GitHub
- [ ] Railway project created
- [ ] Deployment successful
- [ ] Public URL accessible
- [ ] Test image analyzed correctly
- [ ] Results display properly

---

**Ready to deploy? Follow the steps above and you'll be live in 15 minutes!** 🎉
