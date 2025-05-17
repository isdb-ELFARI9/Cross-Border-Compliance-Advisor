"""
Models for Regulation Update API.
"""

from typing import Dict, Any, List, Optional
from api.models.base import APIModel

class RegulationInput(APIModel):
    """Input model for Regulation Update."""
    
    def __init__(self, regulations: Dict[str, Any]):
        self.regulations = regulations
        
    @classmethod
    def from_request(cls, data: Dict[str, Any]) -> 'RegulationInput':
        """Create a RegulationInput model from request data."""
        return cls(
            regulations=data.get("regulations", {})
        )

class RegulationUpdateResponse(APIModel):
    """Response model for Regulation Update."""
    
    def __init__(self, final_review_report: Dict[str, List[Any]]):
        self.final_review_report = final_review_report
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary."""
        return {
            "final_review_report": self.final_review_report
        }
