"""
Regulation Drafting API endpoints.
"""

import json
import os
from pathlib import Path
from fastapi import APIRouter, HTTPException, Request, BackgroundTasks
from api.models.regulation_drafting import RegulationInput, RegulationDraftingResponse
from api.services.orchestrator_service import OrchestratorService
from api.core.logging import logger
from api.core.config import DATA_DIR

router = APIRouter(tags=["regulation-drafting"])

@router.post("/regulation-drafting")
async def process_regulation_drafting(request: Request, background_tasks: BackgroundTasks):
    """
    Process regulations for Shariah compliance analysis.
    """
    orchestrator = OrchestratorService.get_regulation_revision_orchestrator()
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Regulation Revision service not available")
    
    try:
        # Parse JSON manually to avoid Pydantic issues
        body = await request.json()
        regulation_input = RegulationInput.from_request(body)
        
        if not regulation_input.regulations:
            raise HTTPException(status_code=400, detail="Regulations data is required")
        
        # Save input to a temporary file
        temp_input_path = DATA_DIR / "temp_input.json"
        with open(temp_input_path, 'w', encoding='utf-8') as f:
            json.dump(regulation_input.regulations, f, indent=2)
        
        # Process regulations
        updated_regulations = orchestrator.process_regulations(str(temp_input_path))
        
        # Clean up in the background
        background_tasks.add_task(os.remove, temp_input_path)
        
        response = RegulationDraftingResponse(updated_regulations)
        return response.to_dict()
    except Exception as e:
        logger.exception("Error processing regulations")
        raise HTTPException(status_code=500, detail=f"Error processing regulations: {str(e)}")
