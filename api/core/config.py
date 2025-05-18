"""
Configuration settings for the API.
"""

import os
from pathlib import Path

# API settings
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))
DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")

# Root directory
ROOT_DIR = Path(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
DATA_DIR = ROOT_DIR / "data"

# Ensure data directory exists
DATA_DIR.mkdir(exist_ok=True)

# API documentation
API_TITLE = "Cross-Border Compliance Advisor API"
API_DESCRIPTION = "API for Shariah compliance analysis and regulatory management"
API_VERSION = "1.0.0"

# CORS settings
CORS_ALLOW_ORIGINS = ["*"]  # In production, limit this to specific origins
CORS_ALLOW_METHODS = ["*"]
CORS_ALLOW_HEADERS = ["*"]
