"""
Regulation Update API endpoints.
"""

from fastapi import APIRouter, HTTPException, Request
from api.models.regulation_update import RegulationInput, RegulationUpdateResponse
from api.services.orchestrator_service import OrchestratorService
from api.core.logging import logger

router = APIRouter(tags=["regulation-update"])

@router.post("/regulation-update")
async def process_regulation_update(request: Request):
    """
    Analyze regulations for compliance issues.
    """
    orchestrator = OrchestratorService.get_update_revision_orchestrator()
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Update Revision service not available")
    
    try:
        # Parse JSON manually to avoid Pydantic issues
        body = await request.json()
        regulation_input = RegulationInput.from_request(body)
        
        if not regulation_input.regulations:
            raise HTTPException(status_code=400, detail="Regulations data is required")
        
        # Process regulations asynchronously
        result = await orchestrator.orchestrate(regulation_input.regulations)
        return result
    except Exception as e:
        logger.exception("Error analyzing regulations")
        raise HTTPException(status_code=500, detail=f"Error analyzing regulations: {str(e)}")
