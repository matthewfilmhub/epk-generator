# 🚀 Deploy to Vercel - Complete Guide

## 📦 Step 1: Download Files

### Download Complete Package
**[⬇️ Download EPK Generator (49KB)](computer:///mnt/user-data/outputs/epk-generator-complete.tar.gz)**

This includes:
- ✅ Complete source code (backend + frontend)
- ✅ All documentation (11 guides)
- ✅ Configuration files (vercel.json, etc.)
- ✅ Setup scripts (setup.sh, setup.bat)
- ✅ Sample test data
- ✅ Brand guidelines

### Extract the Files

**macOS/Linux:**
```bash
tar -xzf epk-generator-complete.tar.gz
cd epk-generator-complete
```

**Windows:**
```bash
# Use 7-Zip, WinRAR, or Windows built-in extractor
# Right-click → Extract All
# Then open the folder in terminal:
cd epk-generator-complete
```

---

## 🧪 Step 2: Test Locally (Optional - 5 min)

**Recommended before deploying to catch any issues early!**

```bash
# Run setup script
./setup.sh        # macOS/Linux
setup.bat         # Windows

# Start backend (Terminal 1)
cd api
source venv/bin/activate  # Windows: venv\Scripts\activate
python main.py

# Start frontend (Terminal 2)  
cd frontend
npm start

# Visit http://localhost:3000
# Try creating a test EPK
```

✅ If it works locally, deployment will work!

---

## 📤 Step 3: Push to GitHub (5 min)

### 3.1 - Create GitHub Repository

1. Go to: **https://github.com/new**
2. Repository name: `epk-generator`
3. Private: ✅ (Recommended)
4. **Don't** initialize with README
5. Click **"Create repository"**

### 3.2 - Push Your Code

```bash
# In your epk-generator folder
git init
git add .
git commit -m "Initial commit - EPK Generator with Filmhub branding"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/epk-generator.git
git push -u origin main
```

Replace `YOUR-USERNAME` with your actual GitHub username.

---

## 🚀 Step 4: Deploy to Vercel (5 min)

### 4.1 - Sign Up/Login

1. Go to: **https://vercel.com**
2. Click **"Sign Up"** (or "Login")
3. Choose **"Continue with GitHub"** ← Easiest option
4. Authorize Vercel

### 4.2 - Import Project

1. Click **"Add New..."** → **"Project"**
2. Find your **"epk-generator"** repository
3. Click **"Import"**

### 4.3 - Configure (Important!)

Vercel auto-detects most settings. Just verify:

```
✓ Framework Preset: Other
✓ Root Directory: ./
✓ Build Command: (auto-detected)
✓ Output Directory: (auto-detected)
```

### 4.4 - Add Environment Variable

⚠️ **CRITICAL - DON'T SKIP THIS**

Click **"Environment Variables"** section and add:

```
Name:  PLAYWRIGHT_BROWSERS_PATH
Value: /tmp/.cache/ms-playwright
```

Click **"Add"**

### 4.5 - Deploy

1. Click **"Deploy"** button
2. Wait 2-3 minutes ☕
3. Watch the build logs (optional but cool!)
4. Success! You'll get a URL like:
   ```
   https://epk-generator-abc123xyz.vercel.app
   ```

### 4.6 - Test It!

1. Click your deployment URL
2. Try creating an EPK:
   - Fill in film title
   - Upload a poster image
   - Add some team members
   - Generate EPK
3. Download HTML and PDF
4. ✅ If both work, you're done!

---

## ✅ Quick Checklist

Track your progress:

- [ ] Files downloaded and extracted
- [ ] (Optional) Tested locally
- [ ] GitHub account ready
- [ ] GitHub repository created
- [ ] Code pushed to GitHub
- [ ] Vercel account created
- [ ] Repository imported to Vercel
- [ ] Environment variable added
- [ ] Deployment successful
- [ ] Test EPK creation works
- [ ] HTML download works
- [ ] PDF download works

**Time to complete: ~15 minutes**

---

## 🎯 What You'll Get

Once deployed, your team can:

1. **Access from anywhere**: Just share the URL
2. **Create EPKs in 5 minutes**: No more manual HTML editing
3. **Professional output**: Both HTML and PDF versions
4. **Filmhub branding**: Orange, black, white color scheme
5. **No installation**: Works in any browser

---

## 🔧 Troubleshooting

### Problem: Git not installed

**Error:** `git: command not found`

**Fix:**
- **macOS:** `xcode-select --install`
- **Windows:** Download from https://git-scm.com/download/win
- **Linux:** `sudo apt-get install git`

### Problem: Build failed on Vercel

**Error:** Build timeout or failures

**Fix:**
1. Check the build logs in Vercel dashboard
2. Make sure all files were pushed to GitHub
3. Verify `vercel.json` is in root directory
4. Try redeploying (sometimes it's temporary)

### Problem: PDF not generating

**Error:** Playwright browsers not found

**Fix:**
1. Go to Vercel Project → Settings → Environment Variables
2. Verify `PLAYWRIGHT_BROWSERS_PATH` is set to `/tmp/.cache/ms-playwright`
3. Redeploy the project (top right → Redeploy)

### Problem: Can't push to GitHub

**Error:** Authentication failed

**Fix:**
1. Set up SSH keys or use Personal Access Token
2. Guide: https://docs.github.com/en/authentication
3. Or use GitHub Desktop (easier): https://desktop.github.com

### Problem: CORS errors in browser

**Error:** CORS policy blocking

**Fix:**
Your frontend URL needs to match. If you get this, update `api/main.py`:
```python
allow_origins=["https://your-actual-vercel-url.vercel.app"]
```

---

## 💡 Pro Tips

### Custom Domain (Optional)

Want `epk.yourcompany.com` instead of Vercel's URL?

1. Vercel Project → Settings → Domains
2. Add your domain
3. Follow DNS instructions
4. Wait for SSL (automatic)

### Team Access

Add your team in Vercel:

1. Project → Settings → Team
2. Invite members
3. Set permissions

### Automatic Deployments

Every time you push to GitHub `main` branch:
- Vercel automatically redeploys
- Preview deployments for other branches
- Zero downtime deployments

---

## 💰 Cost

### Free Tier (Perfect for Most Teams)
- **$0/month**
- 100 GB bandwidth
- 100 GB-hours functions
- 10-second timeout
- Unlimited projects

### When to Upgrade ($20/month Pro)
- Need longer timeout (60s)
- Higher bandwidth (1TB)
- Team features
- Priority support

**Start free, upgrade if needed!**

---

## 📱 Share with Your Team

After deployment, send your team:

**1. The URL**
```
https://your-epk-generator.vercel.app
```

**2. Quick instructions:**
```
1. Go to the URL
2. Fill in your film details
3. Upload poster and stills
4. Click "Create EPK Project"
5. Download HTML and PDF
```

**3. Sample config for testing:**
Share the `sample_config.json` file so they can try it

---

## 🎓 Next Steps

### Immediate
1. ✅ Test thoroughly with a real film
2. ✅ Train 2-3 team members
3. ✅ Create internal documentation

### This Week
1. Roll out to full team
2. Set up monitoring
3. Collect feedback

### This Month
1. Consider custom domain
2. Add authentication (if needed)
3. Integrate with your storage solution

---

## 📚 Full Documentation

Your complete package includes:

1. **[START_HERE.md](computer:///mnt/user-data/outputs/START_HERE.md)** - Overview
2. **[QUICK_START.md](computer:///mnt/user-data/outputs/QUICK_START.md)** - Getting started
3. **[DEPLOYMENT.md](computer:///mnt/user-data/outputs/DEPLOYMENT.md)** - Detailed deployment
4. **[README.md](computer:///mnt/user-data/outputs/README.md)** - Technical docs
5. **[BRAND_GUIDELINES.md](computer:///mnt/user-data/outputs/BRAND_GUIDELINES.md)** - Brand colors
6. **[COLOR_PALETTE.md](computer:///mnt/user-data/outputs/COLOR_PALETTE.md)** - Color reference

---

## 🆘 Need Help?

### Quick Help
- **Quick questions:** Check [QUICK_START.md](computer:///mnt/user-data/outputs/QUICK_START.md)
- **Technical issues:** See [README.md](computer:///mnt/user-data/outputs/README.md)
- **Deployment problems:** Read full [DEPLOYMENT.md](computer:///mnt/user-data/outputs/DEPLOYMENT.md)

### External Help
- **Vercel Docs:** https://vercel.com/docs
- **GitHub Docs:** https://docs.github.com
- **Vercel Support:** https://vercel.com/support

---

## 🎉 Summary

You now have:
- ✅ Complete EPK Generator application
- ✅ Filmhub brand colors integrated
- ✅ All documentation and guides
- ✅ Step-by-step deployment instructions
- ✅ Troubleshooting solutions

**Just follow the 4 steps above and you'll be live in ~15 minutes!**

---

## 🔗 Essential Links

**Downloads:**
- [📦 Complete Package (49KB)](computer:///mnt/user-data/outputs/epk-generator-complete.tar.gz) ⭐

**External Services:**
- [GitHub (create repo)](https://github.com/new)
- [Vercel (deploy)](https://vercel.com)
- [Git downloads (if needed)](https://git-scm.com)

**Documentation in Package:**
- All guides included in download
- Open any .md file in a text editor or GitHub

---

**Ready?** [⬇️ Download the package](computer:///mnt/user-data/outputs/epk-generator-complete.tar.gz) and follow steps 1-4!

Good luck with your deployment! 🚀🎬
