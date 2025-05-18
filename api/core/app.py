"""
Main application initialization and configuration.
"""

# import sys
import os
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# # Add the project root to Python path first
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

# Now import our modules
from api.core.config import (
    API_TITLE, API_DESCRIPTION, API_VERSION,
    CORS_ALLOW_ORIGINS, CORS_ALLOW_METHODS, CORS_ALLOW_HEADERS
)
from api.core.logging import logger
from api.routes import health, qa_transform, regulation_drafting, regulation_update
from api.services.orchestrator_service import OrchestratorService

# Create FastAPI app without any docs or redoc to avoid pydantic issues
app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION,
    docs_url=None,  # Disable swagger docs to avoid pydantic issues
    redoc_url=None  # Disable redoc to avoid pydantic issues
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=CORS_ALLOW_METHODS,
    allow_headers=CORS_ALLOW_HEADERS,
)

@app.on_event("startup")
async def startup_event():
    """Initialize resources when the application starts"""
    logger.info("Loading orchestrators and resources...")
    
    try:
        # Initialize orchestrator service
        await OrchestratorService.initialize()
        logger.info("All resources loaded successfully")
    except Exception as e:
        logger.error(f"Error initializing resources: {str(e)}")

@app.on_event("shutdown")
async def shutdown_event():
    """Clean up resources when the application shuts down"""
    logger.info("Shutting down and cleaning up resources...")
    OrchestratorService.cleanup()

# Include API routes
app.include_router(health.router)
app.include_router(qa_transform.router, prefix="/api")
app.include_router(regulation_drafting.router, prefix="/api")
app.include_router(regulation_update.router, prefix="/api")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")
