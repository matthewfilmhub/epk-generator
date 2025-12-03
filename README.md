# EPK Generator - Web Application

A professional Electronic Press Kit (EPK) generator for films, deployable to Vercel for team collaboration.

## Features

- 🎬 **Professional EPK Generation**: Create high-quality HTML and PDF press kits
- 🎨 **Genre-Based Theming**: Automatic color schemes based on film genre
- 📤 **Asset Management**: Upload posters, stills, and team photos
- ✅ **Validation**: Real-time validation of required fields and assets
- 📱 **Responsive Design**: Works on desktop and mobile devices
- 🚀 **Cloud Hosting**: Deploy to Vercel for team access

## Project Structure

```
epk-generator/
├── api/                          # Python FastAPI backend
│   ├── main.py                   # API endpoints
│   ├── epk_core.py              # EPK generation logic
│   └── requirements.txt          # Python dependencies
├── frontend/                     # React frontend
│   ├── src/
│   │   ├── App.jsx              # Main React component
│   │   ├── index.js             # React entry point
│   │   └── index.css            # Tailwind CSS
│   ├── public/
│   │   └── index.html           # HTML template
│   └── package.json             # Node dependencies
├── vercel.json                  # Vercel deployment config
└── README.md                    # This file
```

## Local Development

### Prerequisites

- Python 3.9+
- Node.js 16+
- npm or yarn

### Backend Setup

```bash
# Navigate to api directory
cd api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium

# Run the API server
python main.py
# API will be available at http://localhost:8000
```

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm start
# Frontend will be available at http://localhost:3000
```

## Deployment to Vercel

### Option 1: Deploy via Vercel CLI

1. **Install Vercel CLI**
```bash
npm install -g vercel
```

2. **Login to Vercel**
```bash
vercel login
```

3. **Deploy**
```bash
# From the project root directory
vercel

# For production deployment
vercel --prod
```

### Option 2: Deploy via GitHub Integration

1. **Push to GitHub**
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-repo-url>
git push -u origin main
```

2. **Connect to Vercel**
   - Go to [vercel.com](https://vercel.com)
   - Click "New Project"
   - Import your GitHub repository
   - Vercel will auto-detect the configuration
   - Click "Deploy"

### Environment Variables

Set these in Vercel Dashboard (Project Settings → Environment Variables):

```
PLAYWRIGHT_BROWSERS_PATH=/tmp/.cache/ms-playwright
```

### Important Notes for Vercel Deployment

1. **Playwright on Vercel**: The Playwright browser installation is handled automatically through the deployment configuration. The browsers are cached in `/tmp/.cache/ms-playwright`.

2. **Serverless Function Limits**: 
   - Max execution time: 10 seconds (Hobby), 60 seconds (Pro)
   - Max payload: 4.5MB
   - Consider implementing background jobs for large EPK generation

3. **File Storage**: 
   - Temporary files are stored in `/tmp/` which is ephemeral
   - For persistent storage, integrate with:
     - AWS S3
     - Vercel Blob Storage
     - Cloudinary

## API Endpoints

### Health Check
```
GET /
```

### Create Project
```
POST /api/projects/create
Content-Type: multipart/form-data

Body:
- config: JSON string (film configuration)
- poster: File (optional)
- stills: File[] (optional)
- team_photos: File[] (optional)

Response:
{
  "project_id": "uuid",
  "status": "created",
  "message": "...",
  "validation": {
    "is_valid": boolean,
    "errors": string[],
    "warnings": string[]
  }
}
```

### Generate EPK
```
POST /api/projects/{project_id}/generate?generate_pdf=true

Response:
{
  "project_id": "uuid",
  "status": "generated",
  "message": "...",
  "download_urls": {
    "html": "/api/projects/{id}/download/html",
    "pdf": "/api/projects/{id}/download/pdf"
  }
}
```

### Download Files
```
GET /api/projects/{project_id}/download/{file_type}
file_type: "html" | "pdf" | "package"
```

### Validate Project
```
GET /api/projects/{project_id}/validate
```

### Get Configuration Template
```
GET /api/template
```

## Configuration Format

The film configuration follows this structure:

```json
{
  "metadata": {
    "title": "Film Title",
    "tagline": "Compelling tagline",
    "logline": "One-sentence pitch",
    "synopsis": "Full synopsis (2-3 paragraphs)",
    "genre": "Horror",
    "runtime": "90 minutes",
    "rating": "NR",
    "release_date": "2025",
    "language": "English",
    "country": "USA",
    "director": "Director Name"
  },
  "team": [
    {
      "name": "Director Name",
      "role": "Writer/Director",
      "bio": "Brief bio",
      "photo": "path/to/photo.jpg"
    }
  ],
  "awards": [
    {
      "festival_name": "Sundance",
      "award": "Jury Award - Best Feature",
      "year": "2025"
    }
  ],
  "reviews": [
    {
      "quote": "A masterpiece",
      "source": "The Hollywood Reporter",
      "rating": "5"
    }
  ],
  "contact": {
    "distribution_company": "Filmhub",
    "name": "Contact Name",
    "email": "contact@example.com",
    "phone": "(555) 123-4567",
    "website": "https://example.com"
  }
}
```

## Asset Requirements

### Poster
- **Format**: JPG or PNG
- **Recommended Resolution**: 2000x3000px (2:3 aspect ratio)
- **Minimum Resolution**: 1000x1500px

### Production Stills
- **Format**: JPG or PNG
- **Recommended Quantity**: 8-12 images
- **Recommended Resolution**: 1920x1080px
- **Minimum Resolution**: 1280x720px

### Team Photos
- **Format**: JPG or PNG
- **Recommended Resolution**: Square format, 800x800px minimum
- **Naming**: Name files to match team member names for auto-association

## Production Considerations

### Scaling

For production use with multiple concurrent users:

1. **Database Integration**
   - Replace in-memory storage with PostgreSQL/MongoDB
   - Store project metadata and status
   - Track user sessions

2. **Object Storage**
   - Integrate S3/Cloudinary for file storage
   - Generate signed URLs for downloads
   - Implement cleanup jobs for old files

3. **Queue System**
   - Use Bull/BullMQ for background processing
   - Handle long-running EPK generation asynchronously
   - Send email notifications when ready

4. **Authentication**
   - Add user authentication (Auth0, Clerk, or custom)
   - Implement project ownership
   - Add team collaboration features

### Example with Persistent Storage

```python
# Add to api/main.py for S3 integration
import boto3

s3_client = boto3.client('s3')

async def upload_to_s3(file_path: Path, bucket: str, key: str):
    with open(file_path, 'rb') as f:
        s3_client.upload_fileobj(f, bucket, key)
    return f"https://{bucket}.s3.amazonaws.com/{key}"
```

## Troubleshooting

### Playwright Installation Issues

If Playwright fails to install browsers:
```bash
# Install system dependencies (Ubuntu/Debian)
sudo apt-get install -y \
  libnss3 \
  libnspr4 \
  libatk1.0-0 \
  libatk-bridge2.0-0 \
  libcups2 \
  libdrm2 \
  libxkbcommon0 \
  libxcomposite1 \
  libxdamage1 \
  libxfixes3 \
  libxrandr2 \
  libgbm1 \
  libasound2

# Then reinstall
playwright install chromium
```

### CORS Issues

If you encounter CORS errors in development:
- Ensure the frontend is configured with the correct API URL
- Check that CORS middleware in FastAPI allows your frontend origin

### Large File Uploads

For files larger than 4.5MB on Vercel:
- Compress images before upload
- Implement chunked upload
- Consider direct-to-S3 uploads with presigned URLs

## License

MIT License - Feel free to use and modify for your projects.

## Credits

Created for Filmhub's media production and quality control workflow.

## Support

For issues or questions:
- Check the troubleshooting section
- Review API endpoint documentation
- Contact your team administrator
