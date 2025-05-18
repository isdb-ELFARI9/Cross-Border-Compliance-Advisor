"""
Health check endpoints.
"""

from fastapi import APIRouter, HTTPException
from api.services.orchestrator_service import OrchestratorService

router = APIRouter(tags=["health"])

@router.get("/health")
async def health_check():
    """Check if the API is healthy and all services are available."""
    return {
        "status": "healthy",
        "services": OrchestratorService.get_status()
    }
