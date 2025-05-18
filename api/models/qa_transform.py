"""
Models for QA Transform API.
"""

from typing import Dict, Any, List, Optional
from api.models.base import APIModel

class Query(APIModel):
    """Query model for QA Transform."""
    
    def __init__(self, text: str):
        self.text = text
        
    @classmethod
    def from_request(cls, data: Dict[str, Any]) -> 'Query':
        """Create a Query model from request data."""
        return cls(
            text=data.get("text", "")
        )

class QATransformResponse(APIModel):
    """Response model for QA Transform."""
    
    def __init__(self, query: str, analysis_process: Dict[str, Any], final_answer: str):
        self.query = query
        self.analysis_process = analysis_process
        self.final_answer = final_answer
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary."""
        return {
            "query": self.query,
            "analysis_process": self.analysis_process,
            "final_answer": self.final_answer
        }
