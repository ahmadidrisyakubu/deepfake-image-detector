# Railway Deployment Guide

This guide provides detailed step-by-step instructions for deploying your Deepfake Detection Tool on Railway.

## Prerequisites

1. **Railway Account**: Sign up at [railway.app](https://railway.app)
2. **GitHub Account**: You'll need a GitHub account to connect your repository
3. **Git**: Installed on your local machine

## Step-by-Step Deployment

### Step 1: Prepare Your Code

1. **Download/Clone this repository** to your local machine

2. **Navigate to the project directory**:
   ```bash
   cd deepfake-detector
   ```

### Step 2: Initialize Git Repository

1. **Initialize Git** (if not already initialized):
   ```bash
   git init
   ```

2. **Add all files**:
   ```bash
   git add .
   ```

3. **Commit your changes**:
   ```bash
   git commit -m "Initial commit: Deepfake detection app"
   ```

### Step 3: Push to GitHub

1. **Create a new repository on GitHub**:
   - Go to [github.com](https://github.com)
   - Click the "+" icon → "New repository"
   - Name it (e.g., `deepfake-detector`)
   - **Do NOT** initialize with README, .gitignore, or license
   - Click "Create repository"

2. **Link your local repository to GitHub**:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/deepfake-detector.git
   git branch -M main
   git push -u origin main
   ```

   Replace `YOUR_USERNAME` with your actual GitHub username.

### Step 4: Deploy on Railway

1. **Go to Railway**:
   - Visit [railway.app](https://railway.app)
   - Log in or sign up

2. **Create a New Project**:
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - If this is your first time, you'll need to authorize Railway to access your GitHub account

3. **Select Your Repository**:
   - Find and select your `deepfake-detector` repository
   - Click on it to start deployment

4. **Wait for Deployment**:
   - Railway will automatically:
     - Detect the Python environment
     - Install dependencies from `requirements.txt`
     - Download the model from Hugging Face (this may take 5-10 minutes)
     - Start the application using the `Procfile`

5. **Monitor the Build**:
   - Click on the "Deployments" tab to see build logs
   - Watch for any errors
   - The first deployment will take longer due to model download

### Step 5: Configure Your Application

1. **Generate a Domain**:
   - In your Railway project, click on "Settings"
   - Scroll to "Domains"
   - Click "Generate Domain"
   - Railway will provide a public URL (e.g., `your-app.up.railway.app`)

2. **Check Environment Variables** (Optional):
   - Railway automatically sets `PORT`
   - No additional configuration needed for basic deployment

### Step 6: Access Your Application

1. **Open the URL**:
   - Click on the generated domain
   - Your app should load with the beautiful UI

2. **Test the Application**:
   - Upload an image
   - Click "Detect Image"
   - Verify the results

## Important Notes

### Model Download
- **First deployment takes 5-10 minutes** due to model download from Hugging Face
- The model (~400-500 MB) is downloaded automatically
- Subsequent deployments will be faster as Railway caches dependencies

### Memory Requirements
- The app requires approximately **1-2 GB RAM**
- Railway's free tier provides sufficient resources for testing
- For production use, consider upgrading to a paid plan

### Performance Tips
1. **Worker Configuration**: The `Procfile` uses 2 workers. Adjust based on your plan:
   ```
   web: gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --timeout 120
   ```

2. **Timeout Settings**: Set to 120 seconds to handle model loading and inference

3. **Cold Starts**: Railway may put inactive apps to sleep. First request after sleep will be slower.

## Troubleshooting

### Build Fails

**Problem**: Build fails with dependency errors

**Solution**:
- Check `requirements.txt` for correct versions
- Review Railway build logs for specific error messages
- Ensure Python version in `runtime.txt` is supported

### Model Download Fails

**Problem**: "Model not loaded" error

**Solution**:
- Check Railway logs for Hugging Face connection errors
- Ensure Railway has internet access (should be default)
- Try redeploying

### Out of Memory

**Problem**: App crashes with memory errors

**Solution**:
- Reduce workers in `Procfile` to 1
- Upgrade Railway plan for more memory
- Consider using CPU-only inference (already configured)

### Slow Response Times

**Problem**: Predictions take too long

**Solution**:
- First prediction is always slower (model initialization)
- Subsequent predictions should be faster
- Consider upgrading to Railway's GPU instances (paid)

### 413 Error (File Too Large)

**Problem**: Cannot upload large images

**Solution**:
- Check `MAX_CONTENT_LENGTH` in `app.py` (default: 30 MB)
- Railway may have additional limits on free tier
- Compress images before uploading

## Monitoring and Maintenance

### View Logs
```bash
# In Railway dashboard
1. Go to your project
2. Click "Deployments"
3. Select the latest deployment
4. View logs in real-time
```

### Update Your Application

1. **Make changes locally**
2. **Commit and push**:
   ```bash
   git add .
   git commit -m "Description of changes"
   git push
   ```
3. **Railway auto-deploys** on push to main branch

### Rollback

If something goes wrong:
1. Go to "Deployments" in Railway
2. Find a previous working deployment
3. Click "Redeploy"

## Cost Considerations

### Railway Free Tier
- **$5 free credit per month**
- Sufficient for testing and low-traffic apps
- Apps may sleep after inactivity

### Paid Plans
- **Hobby Plan**: $5/month + usage
- **Pro Plan**: $20/month + usage
- Better for production use
- No sleeping
- More resources

## Security Best Practices

1. **Environment Variables**: Store sensitive data in Railway environment variables, not in code
2. **Rate Limiting**: Already configured in the app
3. **HTTPS**: Railway provides automatic HTTPS
4. **Updates**: Keep dependencies updated regularly

## Additional Resources

- [Railway Documentation](https://docs.railway.app/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Hugging Face Model](https://huggingface.co/waleeyd/deepfake-detector)

## Support

If you encounter issues:
1. Check Railway logs first
2. Review this guide
3. Check the main README.md
4. Open an issue on GitHub

---

**Happy Deploying! 🚀**
