from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import sys
import os

# Add the api directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import your main app
from api.main import app as fastapi_app

# Vercel serverless function handler
async def handler(request: Request):
    """
    Vercel serverless function handler
    """
    return await fastapi_app(request)

# Export for Vercel
app = fastapi_app
