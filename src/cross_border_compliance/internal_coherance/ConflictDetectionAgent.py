"""
Conflict Detection Agent
Purpose: Analyzes cross-border contracts for conflicts between different regulatory frameworks and accounting standards.
"""

from typing import List, Dict, Optional
from pydantic import BaseModel, Field
from openai import OpenAI
from ...core.config import settings
import json

class ConflictElement(BaseModel):
    """Model for individual conflict elements."""
    section: str = Field(description="The contract section where conflict was detected")
    conflict_description: str = Field(description="Description of the conflict between regulatory frameworks")
    impact: str = Field(description="Impact of the conflict on contract execution")
    recommendation: str = Field(description="Recommended resolution approach")

class ContractSection(BaseModel):
    """Model for contract section analysis."""
    section_name: str = Field(description="Name of the contract section")
    content: str = Field(description="Content of the section")

class ConflictAnalysisInput(BaseModel):
    """Input model for conflict analysis."""
    contract_section: ContractSection = Field(description="The contract section to analyze")

class ConflictAnalysisResult(BaseModel):
    """Model for conflict analysis results."""
    has_conflicts: bool = Field(description="Whether conflicts exist in the section")
    conflicts: List[ConflictElement] = Field(default_factory=list, description="List of identified conflicts")
    summary: str = Field(description="Summary of conflict analysis")

class ConflictDetectionAgent:
    """Agent for detecting conflicts in cross-border contracts between different regulatory frameworks."""
    
    def __init__(self):
        """Initialize the Conflict Detection agent."""
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.system_prompt = """
You are a Conflict Detection Agent specialized in analyzing cross-border contracts for conflicts between different regulatory frameworks and accounting standards.

Your task is to analyze contract sections and identify potential conflicts between different regulatory frameworks (e.g., AAOIFI vs IFRS, EU regulations vs Islamic finance standards).

For each identified conflict, provide:
1. The specific section where the conflict occurs
2. A clear description of the conflict
3. The potential impact on contract execution
4. A recommended resolution approach

Return your analysis in a structured JSON format with the following fields:
{
    "has_conflicts": boolean,
    "conflicts": [
        {
            "section": "string",
            "conflict_description": "string",
            "impact": "string",
            "recommendation": "string"
        }
    ],
    "summary": "string"
}

IMPORTANT: Your response must be valid JSON that can be parsed by Python's json.loads() function.
"""

    def analyze_conflicts(self, input_data: ConflictAnalysisInput) -> ConflictAnalysisResult:
        """
        Analyze a contract section for conflicts between regulatory frameworks.
        
        Args:
            input_data: ConflictAnalysisInput object containing contract section
            
        Returns:
            ConflictAnalysisResult object containing conflict analysis
        """
        try:
            # Format the user message
            user_message = self._format_user_message(input_data)
            
            # Get analysis from OpenAI
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.2,
                response_format={"type": "json_object"}
            )
            
            # Parse the response
            analysis_data = response.choices[0].message.content
            try:
                json_data = json.loads(analysis_data)
                return ConflictAnalysisResult.parse_obj(json_data)
            except json.JSONDecodeError:
                return ConflictAnalysisResult.parse_raw(analysis_data)
            
        except Exception as e:
            print(f"Error during conflict analysis: {e}")
            raise

    def _format_user_message(self, input_data: ConflictAnalysisInput) -> str:
        """Format the input data into a structured message for the LLM."""
        return f"""
Contract Section: {input_data.contract_section.section_name}
Content:
{input_data.contract_section.content}
""" 