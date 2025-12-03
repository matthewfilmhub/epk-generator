# Quick Start Guide

Get your EPK Generator running in 5 minutes!

## What is this?

The EPK Generator is a web application that creates professional Electronic Press Kits (EPKs) for films. It generates both HTML and PDF versions with:

- Genre-based color themes
- Professional layouts
- Cast & crew sections
- Awards and festival information
- Production stills galleries
- Press quotes and reviews

## For Team Members: Using the Hosted Version

If your admin has already deployed this, just visit your team's URL:

```
https://your-epk-generator.vercel.app
```

Then:

1. **Fill in Film Information**
   - Title, genre, runtime, synopsis
   - Contact details

2. **Upload Assets**
   - Poster (2000x3000px recommended)
   - Production stills (8-12 images)
   - Team photos (optional)

3. **Add Team & Awards**
   - Cast and crew with bios
   - Festival awards
   - Press reviews

4. **Generate & Download**
   - Click "Create EPK Project"
   - Review validation
   - Click "Generate EPK"
   - Download HTML and PDF

## For Developers: Local Setup

### One-Command Setup

**macOS/Linux:**
```bash
./setup.sh
```

**Windows:**
```bash
setup.bat
```

### Manual Setup

**Backend:**
```bash
cd api
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium
python main.py
```

**Frontend:**
```bash
cd frontend
npm install
npm start
```

Visit: `http://localhost:3000`

## For Admins: Deploying to Vercel

### 1. Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR-USERNAME/epk-generator.git
git push -u origin main
```

### 2. Deploy to Vercel

1. Go to [vercel.com](https://vercel.com)
2. Click "New Project"
3. Import your GitHub repository
4. Add environment variable: `PLAYWRIGHT_BROWSERS_PATH=/tmp/.cache/ms-playwright`
5. Click "Deploy"
6. Share the URL with your team!

**Detailed instructions:** See [DEPLOYMENT.md](DEPLOYMENT.md)

## Common Issues

### "Module not found" errors
```bash
# Backend
cd api
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

### "Playwright not found"
```bash
cd api
source venv/bin/activate
playwright install chromium
```

### "CORS error"
Make sure both backend (port 8000) and frontend (port 3000) are running.

### PDF generation fails
Verify Playwright is installed:
```bash
playwright install chromium
```

## Project Structure

```
epk-generator/
├── api/              # Python backend
│   ├── main.py      # API server
│   └── epk_core.py  # EPK generation
├── frontend/         # React app
│   └── src/
│       └── App.jsx  # Main UI
└── vercel.json      # Deployment config
```

## Configuration Examples

### Minimal Configuration

```json
{
  "metadata": {
    "title": "My Film",
    "logline": "A story about...",
    "synopsis": "Full story here...",
    "genre": "Drama",
    "runtime": "90 minutes"
  },
  "contact": {
    "email": "you@example.com"
  }
}
```

### Full Configuration

See `README.md` for complete configuration options.

## Need Help?

- **Setup Issues**: Check `README.md` troubleshooting section
- **Deployment**: See `DEPLOYMENT.md`
- **API Reference**: Check `README.md` API endpoints
- **Team Questions**: Contact your admin

## What's Next?

After basic setup:

1. ✅ Test with a sample film
2. ✅ Customize genre colors (edit `epk_core.py`)
3. ✅ Add authentication for team use
4. ✅ Integrate with your storage solution
5. ✅ Set up automated backups

## Tips for Best Results

### Poster
- Use high resolution (2000x3000px)
- 2:3 aspect ratio
- Professional quality image

### Synopsis
- 2-3 paragraphs
- 200-400 words
- Tell the complete story

### Production Stills
- 8-12 images minimum
- 1920x1080px or higher
- Diverse shots (characters, locations, action)

### Team Bios
- 2-3 sentences each
- Highlight relevant experience
- Include recent work

---

**Ready to create professional EPKs?** Start with the hosted version or set up locally!

Questions? Check the full [README.md](README.md) or [DEPLOYMENT.md](DEPLOYMENT.md)
