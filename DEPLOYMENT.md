# Deployment Guide for EPK Generator

This guide walks through deploying the EPK Generator to Vercel for team access.

## Prerequisites

- Git installed
- GitHub account
- Vercel account (free tier works)
- Basic command line knowledge

## Step-by-Step Deployment

### Step 1: Prepare Your Repository

1. **Create a new GitHub repository**
   - Go to https://github.com/new
   - Name it: `epk-generator`
   - Set to Private (recommended for team use)
   - Don't initialize with README (we have one)

2. **Upload your code to GitHub**

```bash
# Initialize git repository (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - EPK Generator"

# Connect to your GitHub repository
git remote add origin https://github.com/YOUR-USERNAME/epk-generator.git

# Push to GitHub
git push -u origin main
```

### Step 2: Deploy to Vercel

#### Option A: Deploy via Vercel Dashboard (Recommended for beginners)

1. **Go to Vercel**
   - Visit https://vercel.com
   - Sign up or log in (you can use your GitHub account)

2. **Import Project**
   - Click "Add New..." → "Project"
   - Click "Import Git Repository"
   - Find your `epk-generator` repository
   - Click "Import"

3. **Configure Project**
   - Vercel should auto-detect the configuration from `vercel.json`
   - **Framework Preset**: Leave as detected
   - **Root Directory**: Leave as `./`
   - **Build Command**: Leave as detected
   - **Output Directory**: Leave as detected

4. **Environment Variables**
   - Click "Environment Variables"
   - Add: `PLAYWRIGHT_BROWSERS_PATH` = `/tmp/.cache/ms-playwright`
   - Click "Add"

5. **Deploy**
   - Click "Deploy"
   - Wait 2-3 minutes for deployment to complete
   - You'll get a URL like: `https://epk-generator-xxx.vercel.app`

#### Option B: Deploy via Vercel CLI (For advanced users)

```bash
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Deploy
vercel

# Follow the prompts:
# - Set up and deploy? Yes
# - Which scope? (select your account)
# - Link to existing project? No
# - Project name? epk-generator
# - Directory? ./
# - Override settings? No

# For production deployment
vercel --prod
```

### Step 3: Configure Team Access

1. **Add Team Members**
   - In Vercel Dashboard, go to your project
   - Click "Settings" → "Team"
   - Click "Invite Member"
   - Enter team member emails
   - Set their role (Viewer, Developer, or Admin)

2. **Share the URL**
   - Copy your deployment URL
   - Share with your team
   - Example: `https://epk-generator-xxx.vercel.app`

### Step 4: Test the Deployment

1. **Visit your URL**
   - Open the deployment URL in a browser

2. **Test EPK Creation**
   - Fill in film information
   - Upload a sample poster and stills
   - Click "Create EPK Project"
   - Review validation results
   - Generate EPK
   - Download HTML and PDF

3. **Verify PDF Generation**
   - Check that PDF downloads correctly
   - Verify formatting is preserved
   - Test on different devices

## Common Deployment Issues

### Issue 1: Build Failed

**Error**: Build timeout or dependency installation failure

**Solution**:
```bash
# Test build locally first
cd frontend
npm install
npm run build

# If successful, push to GitHub and redeploy
```

### Issue 2: API Routes Not Working

**Error**: 404 on `/api/*` endpoints

**Solution**:
- Check `vercel.json` is in root directory
- Verify `api/main.py` exists
- Check Vercel function logs in Dashboard

### Issue 3: Playwright Not Found

**Error**: Playwright browsers not installed

**Solution**:
- Verify environment variable is set:
  `PLAYWRIGHT_BROWSERS_PATH=/tmp/.cache/ms-playwright`
- Check that `requirements.txt` includes playwright
- Redeploy to trigger fresh installation

### Issue 4: CORS Errors

**Error**: CORS policy blocking requests

**Solution**:
In `api/main.py`, update CORS configuration:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-vercel-app.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Issue 5: Large Files Timing Out

**Error**: Request timeout on file upload

**Solution**:
- Compress images before upload
- Upgrade to Vercel Pro for longer timeout (60s vs 10s)
- Or implement chunked uploads

## Production Best Practices

### 1. Environment Management

Create separate environments:

```bash
# Development
vercel --dev

# Preview (for testing)
git push origin feature-branch
# Vercel auto-deploys preview

# Production
git push origin main
# Vercel auto-deploys production
```

### 2. Custom Domain

Add a custom domain:
1. Go to Project Settings → Domains
2. Add your domain: `epk.yourcompany.com`
3. Follow DNS configuration instructions
4. Update CORS settings to include custom domain

### 3. Monitoring

Enable monitoring:
1. Go to Project Settings → Analytics
2. Enable Web Analytics
3. Monitor:
   - Page views
   - API response times
   - Error rates
   - Bandwidth usage

### 4. Security

Implement authentication:
```bash
# Install Auth library
npm install @clerk/clerk-react

# Or use Vercel's built-in auth
npm install @vercel/auth
```

Then add authentication to protect routes.

### 5. Persistent Storage

For production, add persistent storage:

**Option A: Vercel Blob Storage**
```bash
npm install @vercel/blob
```

**Option B: AWS S3**
```bash
pip install boto3
```

**Option C: Cloudinary**
```bash
pip install cloudinary
```

## Updating the Application

### Deploy Updates

```bash
# Make your changes
git add .
git commit -m "Description of changes"
git push origin main

# Vercel automatically deploys
```

### Rollback

If something goes wrong:
1. Go to Vercel Dashboard
2. Click "Deployments"
3. Find previous working deployment
4. Click "..." → "Promote to Production"

## Cost Considerations

### Free Tier Limits (Hobby)
- **Bandwidth**: 100 GB/month
- **Function Execution**: 100 GB-hours
- **Function Duration**: 10 seconds max
- **Serverless Function Size**: 50 MB
- **Projects**: Unlimited

### When to Upgrade to Pro ($20/month)
- Need longer function timeouts (60s)
- Higher bandwidth requirements (1 TB)
- Team collaboration features
- Priority support
- Custom usage limits

## Team Workflow

### Recommended Git Workflow

```bash
# Create feature branch
git checkout -b feature/new-genre-colors

# Make changes
# ... edit files ...

# Commit and push
git add .
git commit -m "Add new genre color schemes"
git push origin feature/new-genre-colors

# Vercel creates preview deployment
# Test at: https://epk-generator-git-feature-xxx.vercel.app

# After testing, merge to main
git checkout main
git merge feature/new-genre-colors
git push origin main

# Production deployment happens automatically
```

### Code Review Process

1. Create feature branch
2. Push to GitHub
3. Vercel creates preview URL
4. Team reviews preview
5. Approve and merge to main
6. Vercel deploys to production

## Support Resources

- **Vercel Documentation**: https://vercel.com/docs
- **Vercel Support**: https://vercel.com/support
- **Vercel Community**: https://github.com/vercel/vercel/discussions
- **Project Issues**: Create issues in your GitHub repository

## Next Steps

After successful deployment:

1. ✅ Test all features
2. ✅ Share URL with team
3. ✅ Set up monitoring
4. ✅ Configure custom domain (optional)
5. ✅ Add authentication (for production)
6. ✅ Implement persistent storage (for production)
7. ✅ Set up backup strategy

## Maintenance Schedule

- **Weekly**: Review error logs
- **Monthly**: Check bandwidth usage
- **Quarterly**: Review and update dependencies
- **As needed**: Scale resources based on usage

---

Need help? Check the main README.md or create an issue in your repository.
