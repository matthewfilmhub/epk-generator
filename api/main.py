#!/usr/bin/env python3
"""
FastAPI backend for EPK Generator
Handles file uploads, EPK generation, and serves generated files
"""

from fastapi import FastAPI, UploadFile, File, Form, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
import json
import shutil
import tempfile
import zipfile
from pathlib import Path
from datetime import datetime
import uuid
import logging

# Import the EPK generator
import sys
sys.path.append(os.path.dirname(__file__))
from epk_core import EPKGenerator, ValidationResult

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="EPK Generator API", version="1.0.0")

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Temporary storage for projects
PROJECTS_DIR = Path(tempfile.gettempdir()) / "epk_projects"
PROJECTS_DIR.mkdir(exist_ok=True)

# Store active projects in memory (use Redis in production)
active_projects = {}


class FilmConfig(BaseModel):
    """Film configuration model"""
    metadata: Dict[str, Any]
    team: Optional[List[Dict[str, Any]]] = []
    awards: Optional[List[Dict[str, Any]]] = []
    festivals: Optional[List[Dict[str, Any]]] = []
    reviews: Optional[List[Dict[str, Any]]] = []
    press_coverage: Optional[List[Dict[str, Any]]] = []
    distribution: Optional[Dict[str, Any]] = {}
    technical: Optional[Dict[str, Any]] = {}
    contact: Dict[str, Any]


class ProjectResponse(BaseModel):
    """Response model for project operations"""
    project_id: str
    status: str
    message: str
    validation: Optional[Dict[str, Any]] = None
    download_urls: Optional[Dict[str, str]] = None


@app.get("/")
async def root():
    """API health check"""
    return {
        "status": "online",
        "service": "EPK Generator API",
        "version": "1.0.0"
    }


@app.post("/api/projects/create", response_model=ProjectResponse)
async def create_project(
    config: str = Form(...),
    poster: Optional[UploadFile] = File(None),
    stills: Optional[List[UploadFile]] = File(None),
    team_photos: Optional[List[UploadFile]] = File(None)
):
    """
    Create a new EPK project
    Accepts configuration JSON and asset files
    """
    try:
        # Generate unique project ID
        project_id = str(uuid.uuid4())
        project_dir = PROJECTS_DIR / project_id
        project_dir.mkdir(parents=True, exist_ok=True)
        
        # Parse configuration
        config_data = json.loads(config)
        
        # Setup project structure
        epk = EPKGenerator(str(project_dir))
        epk.setup_project_structure()
        
        # Save configuration
        config_file = project_dir / "film_config.json"
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=2)
        
        # Save uploaded assets
        assets_saved = {}
        
        # Save poster
        if poster:
            poster_path = project_dir / "assets" / "images" / "posters" / poster.filename
            with open(poster_path, "wb") as f:
                shutil.copyfileobj(poster.file, f)
            assets_saved['poster'] = poster.filename
        
        # Save stills
        if stills:
            stills_saved = []
            for still in stills:
                still_path = project_dir / "assets" / "images" / "stills" / still.filename
                with open(still_path, "wb") as f:
                    shutil.copyfileobj(still.file, f)
                stills_saved.append(still.filename)
            assets_saved['stills'] = stills_saved
        
        # Save team photos
        if team_photos:
            photos_saved = []
            for photo in team_photos:
                # Determine if cast or crew based on filename or use crew as default
                photo_dir = project_dir / "assets" / "images" / "crew"
                photo_path = photo_dir / photo.filename
                with open(photo_path, "wb") as f:
                    shutil.copyfileobj(photo.file, f)
                photos_saved.append(photo.filename)
                
                # Update config with photo path
                for member in config_data.get('team', []):
                    if photo.filename.lower().startswith(member.get('name', '').lower().replace(' ', '_')):
                        member['photo'] = f"assets/images/crew/{photo.filename}"
            
            assets_saved['team_photos'] = photos_saved
            
            # Save updated config with photo paths
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=2)
        
        # Store project info
        active_projects[project_id] = {
            'created_at': datetime.now().isoformat(),
            'film_title': config_data.get('metadata', {}).get('title', 'Unknown'),
            'status': 'created',
            'assets': assets_saved
        }
        
        # Validate project
        epk.load_config(str(config_file))
        validation = epk.validate_assets()
        
        return ProjectResponse(
            project_id=project_id,
            status="created",
            message=f"Project created successfully: {config_data.get('metadata', {}).get('title')}",
            validation={
                'is_valid': validation.is_valid,
                'errors': validation.errors,
                'warnings': validation.warnings
            }
        )
        
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON configuration")
    except Exception as e:
        logger.error(f"Error creating project: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/projects/{project_id}/generate", response_model=ProjectResponse)
async def generate_epk(
    project_id: str,
    generate_pdf: bool = True,
    background_tasks: BackgroundTasks = None
):
    """
    Generate EPK files (HTML only on Vercel - PDF requires external service)
    """
    try:
        project_dir = PROJECTS_DIR / project_id
        
        if not project_dir.exists():
            raise HTTPException(status_code=404, detail="Project not found")
        
        config_file = project_dir / "film_config.json"
        if not config_file.exists():
            raise HTTPException(status_code=400, detail="Configuration file not found")
        
        # Generate EPK
        epk = EPKGenerator(str(project_dir))
        epk.load_config(str(config_file))
        
        # Validate before generating
        validation = epk.validate_assets()
        if not validation.is_valid:
            raise HTTPException(
                status_code=400,
                detail={
                    'message': 'Validation failed',
                    'errors': validation.errors
                }
            )
        
        # Generate HTML
        html_path = epk.generate_html()
        
        # Note: PDF generation not available on Vercel free tier
        # Users can print HTML to PDF from their browser
        # Or use a browser extension
        pdf_path = None
        pdf_note = None
        if generate_pdf:
            pdf_note = "PDF generation not available on Vercel. Use your browser's 'Print to PDF' feature on the HTML version."
        
        # Update project status
        if project_id in active_projects:
            active_projects[project_id]['status'] = 'generated'
            active_projects[project_id]['generated_at'] = datetime.now().isoformat()
        
        # Prepare download URLs
        download_urls = {
            'html': f"/api/projects/{project_id}/download/html"
        }
        
        response_message = "EPK generated successfully (HTML only)"
        if pdf_note:
            response_message += f". {pdf_note}"
        
        return ProjectResponse(
            project_id=project_id,
            status="generated",
            message=response_message,
            download_urls=download_urls
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating EPK: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/projects/{project_id}/validate")
async def validate_project(project_id: str):
    """
    Validate project assets without generating EPK
    """
    try:
        project_dir = PROJECTS_DIR / project_id
        
        if not project_dir.exists():
            raise HTTPException(status_code=404, detail="Project not found")
        
        config_file = project_dir / "film_config.json"
        epk = EPKGenerator(str(project_dir))
        epk.load_config(str(config_file))
        
        validation = epk.validate_assets()
        
        return {
            'project_id': project_id,
            'is_valid': validation.is_valid,
            'errors': validation.errors,
            'warnings': validation.warnings
        }
        
    except Exception as e:
        logger.error(f"Error validating project: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/projects/{project_id}/download/{file_type}")
async def download_file(project_id: str, file_type: str):
    """
    Download generated EPK files
    """
    try:
        project_dir = PROJECTS_DIR / project_id
        
        if not project_dir.exists():
            raise HTTPException(status_code=404, detail="Project not found")
        
        if file_type == "html":
            file_path = project_dir / "output" / "html" / "index.html"
            media_type = "text/html"
            filename = f"{active_projects.get(project_id, {}).get('film_title', 'film')}_epk.html"
        elif file_type == "pdf":
            file_path = project_dir / "output" / "pdf" / "epk.pdf"
            media_type = "application/pdf"
            filename = f"{active_projects.get(project_id, {}).get('film_title', 'film')}_epk.pdf"
        elif file_type == "package":
            # Create a zip package with all assets
            return await download_package(project_id)
        else:
            raise HTTPException(status_code=400, detail="Invalid file type")
        
        if not file_path.exists():
            raise HTTPException(status_code=404, detail=f"{file_type.upper()} file not found. Generate EPK first.")
        
        return FileResponse(
            path=str(file_path),
            media_type=media_type,
            filename=filename
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error downloading file: {e}")
        raise HTTPException(status_code=500, detail=str(e))


async def download_package(project_id: str):
    """
    Download complete EPK package as ZIP
    """
    try:
        project_dir = PROJECTS_DIR / project_id
        output_dir = project_dir / "output"
        
        # Create ZIP file
        zip_path = project_dir / "epk_package.zip"
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Add HTML
            html_file = output_dir / "html" / "index.html"
            if html_file.exists():
                zipf.write(html_file, "index.html")
            
            # Add PDF
            pdf_file = output_dir / "pdf" / "epk.pdf"
            if pdf_file.exists():
                zipf.write(pdf_file, "epk.pdf")
            
            # Add all assets
            assets_dir = project_dir / "assets"
            for root, dirs, files in os.walk(assets_dir):
                for file in files:
                    file_path = Path(root) / file
                    arcname = file_path.relative_to(project_dir)
                    zipf.write(file_path, arcname)
        
        film_title = active_projects.get(project_id, {}).get('film_title', 'film')
        
        return FileResponse(
            path=str(zip_path),
            media_type="application/zip",
            filename=f"{film_title}_epk_package.zip"
        )
        
    except Exception as e:
        logger.error(f"Error creating package: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/projects/{project_id}/status")
async def get_project_status(project_id: str):
    """
    Get project status and information
    """
    if project_id not in active_projects:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return {
        'project_id': project_id,
        **active_projects[project_id]
    }


@app.delete("/api/projects/{project_id}")
async def delete_project(project_id: str):
    """
    Delete a project and its files
    """
    try:
        project_dir = PROJECTS_DIR / project_id
        
        if project_dir.exists():
            shutil.rmtree(project_dir)
        
        if project_id in active_projects:
            del active_projects[project_id]
        
        return {"status": "deleted", "project_id": project_id}
        
    except Exception as e:
        logger.error(f"Error deleting project: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/template")
async def get_config_template():
    """
    Get the configuration template
    """
    template = {
        "metadata": {
            "title": "",
            "tagline": "",
            "logline": "",
            "synopsis": "",
            "genre": "",
            "runtime": "",
            "rating": "NR",
            "release_date": "",
            "language": "English",
            "country": "USA",
            "director": ""
        },
        "team": [
            {
                "name": "",
                "role": "",
                "bio": "",
                "photo": ""
            }
        ],
        "awards": [],
        "festivals": [],
        "reviews": [],
        "press_coverage": [],
        "distribution": {
            "theatrical_release": "",
            "digital_release": "",
            "platforms": [],
            "territories": []
        },
        "technical": {
            "aspect_ratio": "16:9",
            "sound": "5.1 Surround",
            "color": "Color"
        },
        "contact": {
            "distribution_company": "Filmhub",
            "name": "",
            "email": "",
            "phone": "",
            "website": ""
        }
    }
    
    return template


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
