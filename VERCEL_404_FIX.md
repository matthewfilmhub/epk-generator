# 🔧 Fixing Vercel 404 Error

## The Problem

You're seeing a 404 error because Vercel has limitations with Python serverless functions and the current project structure needs adjustment.

## ✅ Solution: Deploy Frontend Only (Recommended)

The easiest solution is to deploy just the frontend to Vercel and run the backend separately when needed, or use a different approach.

### Option 1: Frontend-Only on Vercel (Best for Now)

**Step 1: Update `vercel.json`**

Replace your `vercel.json` with this simpler version:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "frontend/package.json",
      "use": "@vercel/static-build",
      "config": {
        "distDir": "build"
      }
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/frontend/$1"
    }
  ]
}
```

**Step 2: Add Build Script**

Add this to `frontend/package.json` in the "scripts" section:

```json
"scripts": {
  "start": "react-scripts start",
  "build": "react-scripts build",
  "vercel-build": "npm install && npm run build"
}
```

**Step 3: Set Root Directory in Vercel**

1. In Vercel dashboard, go to Project Settings
2. Under "Build & Development Settings"
3. Set **Root Directory** to: `frontend`
4. Save and redeploy

**Step 4: Run Backend Locally or on Alternative Service**

For the backend, you have options:
- Run locally when creating EPKs
- Deploy to Railway.app (free Python hosting)
- Deploy to Render.com (free tier available)
- Use Google Cloud Run (pay-as-you-go)

---

### Option 2: Split Deployment (Frontend + Backend Separate)

**Frontend on Vercel:**
- Deploy just the `frontend` folder
- Fast, free, reliable

**Backend Options:**

#### Railway.app (Easiest)
1. Go to https://railway.app
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repo
5. Choose the `api` folder
6. Add environment variable: `PLAYWRIGHT_BROWSERS_PATH=/tmp/.cache/ms-playwright`
7. Railway will give you a URL like: `https://your-app.railway.app`

#### Render.com
1. Go to https://render.com
2. New → Web Service
3. Connect GitHub repo
4. Root Directory: `api`
5. Build Command: `pip install -r requirements.txt && playwright install chromium`
6. Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

#### Then Connect Frontend to Backend

Update `frontend/src/App.jsx`:

```javascript
// At the top of the file
const API_URL = process.env.REACT_APP_API_URL || 'https://your-backend-url.railway.app';
```

Add to `frontend/.env.production`:
```
REACT_APP_API_URL=https://your-backend-url.railway.app
```

---

### Option 3: All-in-One on Railway or Render

Deploy the entire project to a service that better supports Python + Node:

**Railway.app** (Recommended)
1. Go to https://railway.app
2. New Project → Deploy from GitHub
3. It will detect both frontend and backend
4. Configure both services
5. Link them together

**Render.com**
Similar process - it supports monorepos

---

## 🚀 Quick Fix Right Now

**Immediate Solution to Get Running:**

1. **Deploy Frontend Only to Vercel:**

```bash
# In your project root
cd frontend
vercel

# Follow prompts, deploy just the frontend folder
```

2. **Run Backend Locally:**

```bash
# In another terminal
cd api
source venv/bin/activate
python main.py

# Your backend runs at http://localhost:8000
```

3. **Test Locally:**

The frontend on Vercel will try to connect to your local backend when you're testing.

---

## 📝 Recommended Approach

For production use, I recommend:

1. **Frontend → Vercel** (free, fast)
2. **Backend → Railway.app** (free tier, easy Python support)
3. Connect them via environment variable

This gives you:
- ✅ Free hosting for both
- ✅ Easy deployment
- ✅ Automatic HTTPS
- ✅ Good performance
- ✅ Simple to update

---

## 🔄 Updated Deployment Steps

### Deploy Frontend to Vercel

1. Update `vercel.json`:
```json
{
  "buildCommand": "cd frontend && npm install && npm run build",
  "outputDirectory": "frontend/build",
  "devCommand": "cd frontend && npm start",
  "installCommand": "cd frontend && npm install"
}
```

2. In Vercel Dashboard:
   - Settings → General → Root Directory: `frontend`
   - Redeploy

### Deploy Backend to Railway

1. Create `railway.json` in `api` folder:
```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "uvicorn main:app --host 0.0.0.0 --port $PORT",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

2. Create `Procfile` in `api` folder:
```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

3. Push to GitHub, connect to Railway

### Connect Them

In `frontend/src/App.jsx`:
```javascript
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
```

Set in Vercel environment variables:
```
REACT_APP_API_URL = https://your-app.railway.app
```

---

## ✅ Testing Your Fix

After redeploying:

1. Visit your Vercel URL
2. Check browser console (F12) for errors
3. Verify API calls are going to the right URL
4. Test creating an EPK

---

## 🆘 Still Having Issues?

Try this diagnostic:

1. **Check Vercel Build Logs**
   - Vercel Dashboard → Deployments → Click latest → View Build Logs
   - Look for errors

2. **Check Function Logs**
   - Vercel Dashboard → Functions
   - See if API routes are being called

3. **Check Browser Console**
   - F12 → Console tab
   - Look for network errors

4. **Test API Directly**
   - Try visiting: `https://your-app.vercel.app/api/`
   - Should return API health check

---

## 💡 Why This Happened

Vercel has specific requirements for Python serverless functions:
- Limited to 50MB
- 10-second timeout on free tier
- Specific file structure needed
- Cold starts can cause issues

For a full-stack Python + React app, using separate services for frontend and backend is actually more reliable and easier to maintain.

---

## 📞 Need More Help?

1. Share your Vercel build logs
2. Check which approach you want to take
3. I can help configure the specific deployment method

The **Railway.app + Vercel split** is the easiest and most reliable approach!
