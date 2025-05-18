"""
QA Transform API endpoints.
"""

from fastapi import APIRouter, HTTPException, Request
from api.models.qa_transform import Query, QATransformResponse
from api.services.orchestrator_service import OrchestratorService
from api.core.logging import logger

router = APIRouter(tags=["qa-transform"])

@router.post("/qa-transform")
async def process_qa_query(request: Request):
    """
    Process a regulatory query and get a comprehensive answer.
    """
    orchestrator = OrchestratorService.get_qa_transform_orchestrator()
    if not orchestrator:
        raise HTTPException(status_code=503, detail="QA Transform service not available")
    
    try:
        # Parse JSON manually to avoid Pydantic issues
        body = await request.json()
        query = Query.from_request(body)
        
        if not query.text:
            raise HTTPException(status_code=400, detail="Query text is required")
        
        result = orchestrator.process_query(query.text)
        return result
    except Exception as e:
        logger.exception("Error processing query")
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")
