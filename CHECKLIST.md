# Quick Deployment Checklist

Print this and check off as you go!

## 📥 1. Download & Extract

- [ ] [Download package](computer:///mnt/user-data/outputs/epk-generator-complete.tar.gz) (49KB)
- [ ] Extract to folder
- [ ] `cd epk-generator-complete`

## 🧪 2. Test Locally (Optional - 5 min)

- [ ] Run `./setup.sh` (or `setup.bat` on Windows)
- [ ] Start backend: `cd api && python main.py`
- [ ] Start frontend: `cd frontend && npm start`
- [ ] Visit http://localhost:3000
- [ ] Create test EPK ✓

## 📤 3. Push to GitHub (5 min)

- [ ] Create repo at https://github.com/new
- [ ] Name: `epk-generator`
- [ ] Private: ✓
- [ ] Commands:
  ```bash
  git init
  git add .
  git commit -m "Initial commit"
  git remote add origin YOUR-REPO-URL
  git push -u origin main
  ```
- [ ] Verify on GitHub

## 🚀 4. Deploy to Vercel (5 min)

- [ ] Go to https://vercel.com
- [ ] Sign up with GitHub
- [ ] Import `epk-generator` repo
- [ ] **Add environment variable:**
  ```
  PLAYWRIGHT_BROWSERS_PATH = /tmp/.cache/ms-playwright
  ```
- [ ] Click "Deploy"
- [ ] Wait for build ☕

## ✅ 5. Test Deployment

- [ ] Visit deployment URL
- [ ] Create EPK
- [ ] Download HTML works ✓
- [ ] Download PDF works ✓

## 👥 6. Share with Team

- [ ] Copy deployment URL: _________________
- [ ] Share with team
- [ ] Provide quick instructions

---

## Your Info

**URL:** ___________________________________

**GitHub:** ___________________________________

**Deployed:** ___________________________________

**By:** ___________________________________

---

✅ **Done in ~15 minutes!**

Full guide: [DEPLOY_NOW.md](computer:///mnt/user-data/outputs/DEPLOY_NOW.md)
