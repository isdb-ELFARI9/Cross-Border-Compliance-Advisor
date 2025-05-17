"""
Models for Regulation Drafting API.
"""

from typing import Dict, Any, List, Optional
from api.models.base import APIModel

class RegulationInput(APIModel):
    """Input model for Regulation Drafting."""
    
    def __init__(self, regulations: Dict[str, Any]):
        self.regulations = regulations
        
    @classmethod
    def from_request(cls, data: Dict[str, Any]) -> 'RegulationInput':
        """Create a RegulationInput model from request data."""
        return cls(
            regulations=data.get("regulations", {})
        )

class RegulationDraftingResponse(APIModel):
    """Response model for Regulation Drafting."""
    
    def __init__(self, processed_regulations: List[Dict[str, Any]]):
        self.processed_regulations = processed_regulations
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary."""
        return {
            "processed_regulations": self.processed_regulations
        }
