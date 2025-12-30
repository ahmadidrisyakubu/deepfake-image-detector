# Railway Deployment Guide

This guide will walk you through deploying the Deepfake Detector to Railway step by step.

## Prerequisites

- A GitHub account
- A Railway account (sign up at [railway.app](https://railway.app))
- Git installed on your computer

## Step 1: Prepare Your Repository

### 1.1 Initialize Git Repository

```bash
cd deepfake-detector
git init
git add .
git commit -m "Initial commit: Deepfake detector application"
```

### 1.2 Create GitHub Repository

1. Go to [GitHub](https://github.com) and log in
2. Click the "+" icon in the top right and select "New repository"
3. Name it `deepfake-detector` (or your preferred name)
4. **Do NOT** initialize with README, .gitignore, or license (we already have these)
5. Click "Create repository"

### 1.3 Push to GitHub

```bash
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/deepfake-detector.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username.

## Step 2: Deploy to Railway

### 2.1 Sign Up / Log In to Railway

1. Go to [railway.app](https://railway.app)
2. Click "Login" and sign in with GitHub
3. Authorize Railway to access your GitHub repositories

### 2.2 Create New Project

1. Click "New Project" on your Railway dashboard
2. Select "Deploy from GitHub repo"
3. Choose the `deepfake-detector` repository you just created
4. Railway will automatically detect it's a Python application

### 2.3 Configure the Project

Railway should automatically:
- Detect `requirements.txt` and install dependencies
- Detect `Procfile` and use it to start the application
- Use `runtime.txt` to set the Python version
- Assign a port via the `PORT` environment variable

**No additional configuration is needed!**

### 2.4 Wait for Deployment

1. Railway will start building your application
2. This process takes **5-15 minutes** due to:
   - Installing PyTorch (~1GB)
   - Installing Transformers and dependencies
   - Building the application

3. Watch the build logs in the Railway dashboard
4. Look for messages like:
   ```
   Building...
   Installing dependencies...
   Starting application...
   ```

### 2.5 Get Your Public URL

1. Once deployed, click on your project in Railway
2. Go to the "Settings" tab
3. Scroll to "Domains"
4. Click "Generate Domain"
5. Railway will provide a URL like: `https://your-app-name.up.railway.app`

## Step 3: Test Your Deployment

1. Open the Railway-provided URL in your browser
2. You should see the Deepfake Detector interface
3. Upload a test image
4. Click "Analyze Image"
5. **Note**: The first request may take 30-60 seconds as the model downloads from Hugging Face

## Important Notes

### Memory Requirements

The application requires at least **2GB RAM**. Railway's free tier provides:
- **512MB RAM** (Starter plan) - **NOT SUFFICIENT**
- **8GB RAM** (Developer plan) - Recommended

If you encounter memory errors, you'll need to upgrade your Railway plan.

### Model Download

On the first run, the application will download the model from Hugging Face (~500MB). This happens automatically and only once. The model is cached for subsequent requests.

### Build Time

Expect the initial deployment to take 10-15 minutes due to:
- Large dependencies (PyTorch, Transformers)
- Model download on first request

### Cost Considerations

Railway pricing (as of 2024):
- **Free Trial**: $5 credit (may not be enough for full deployment)
- **Developer Plan**: $20/month with $5 included usage
- **Usage-based**: ~$0.000231/GB-hour for memory

For this application, expect costs around $10-15/month on the Developer plan.

## Troubleshooting

### Build Fails

**Error**: `Out of memory during build`

**Solution**: 
- Upgrade to Railway's Developer plan
- Or use a different hosting platform with more resources

### Model Download Timeout

**Error**: `Connection timeout when downloading model`

**Solution**:
- This is usually temporary
- Wait a few minutes and try again
- Check Railway's status page for outages

### Application Crashes

**Error**: `Application error` or `502 Bad Gateway`

**Solution**:
1. Check Railway logs for error messages
2. Ensure all dependencies are in `requirements.txt`
3. Verify the `Procfile` is correct
4. Check that the PORT environment variable is being used

### Slow First Request

**Expected Behavior**: The first request after deployment takes 30-60 seconds because:
1. The model downloads from Hugging Face
2. The model loads into memory
3. PyTorch initializes

Subsequent requests will be much faster (1-3 seconds).

## Alternative Deployment Options

If Railway doesn't work for you, consider these alternatives:

### 1. Heroku
- Similar to Railway
- Requires Heroku CLI
- May need paid dyno for sufficient memory

### 2. Google Cloud Run
- Serverless option
- Pay per request
- Requires Docker knowledge

### 3. AWS EC2
- Full control
- More complex setup
- Cost-effective for high traffic

### 4. DigitalOcean App Platform
- Similar to Railway
- Fixed pricing
- Good for production apps

## Updating Your Deployment

When you make changes to your code:

```bash
git add .
git commit -m "Description of changes"
git push origin main
```

Railway will automatically detect the changes and redeploy your application.

## Environment Variables (Optional)

If you need to add environment variables:

1. Go to your Railway project
2. Click on "Variables" tab
3. Add your variables (e.g., API keys, secrets)

For this application, no additional environment variables are required.

## Monitoring

Railway provides:
- **Logs**: Real-time application logs
- **Metrics**: CPU, Memory, Network usage
- **Deployments**: History of all deployments

Access these from your Railway project dashboard.

## Support

If you encounter issues:

1. Check Railway's [documentation](https://docs.railway.app)
2. Visit Railway's [Discord community](https://discord.gg/railway)
3. Review the application logs in Railway dashboard
4. Check this project's GitHub issues

## Next Steps

After successful deployment:

1. **Add a custom domain** (optional)
   - Go to Settings > Domains in Railway
   - Add your custom domain
   - Configure DNS records

2. **Monitor usage**
   - Keep an eye on memory and CPU usage
   - Set up alerts for high usage

3. **Optimize performance**
   - Consider caching frequently analyzed images
   - Implement a queue system for high traffic

4. **Enhance security**
   - Add authentication if needed
   - Implement API key protection
   - Set up HTTPS (Railway does this automatically)

Congratulations! Your Deepfake Detector is now live! 🎉
