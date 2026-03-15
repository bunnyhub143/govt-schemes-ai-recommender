"""
Vercel serverless entry point for Flask app.
"""
import os
import sys
from pathlib import Path

# Add project root to path so imports work
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

# Set env vars for production
os.environ.setdefault("FLASK_ENV", "production")

from dotenv import load_dotenv
load_dotenv(project_root / ".env")

from app import create_app

app = create_app()

# Vercel expects the WSGI app as 'app'
