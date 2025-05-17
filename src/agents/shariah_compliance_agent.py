"""
Shariah Compliance Checker Agent
Purpose: Evaluates bank rules and policies for compliance with AAOIFI Shariah Standards.
"""

from typing import List, Optional
from pydantic import BaseModel, Field
from openai import OpenAI
from ..core.config import settings
import json

class ComplianceResult(BaseModel):
    """Model for Shariah compliance analysis results."""
    compliance_status: str = Field(
        description="Compliance status: compliant, partially_compliant, or non_compliant",
        pattern="^(compliant|partially_compliant|non_compliant)$"
    )
    justification: str = Field(description="Explanation based on the SS summary")
    referenced_clauses: List[str] = Field(
        default_factory=list,
        description="List of key SS clauses that informed the decision"
    )

class ComplianceInput(BaseModel):
    """Input model for compliance analysis."""
    rule_text: str = Field(description="The bank's internal rule or policy to analyze")
    ss_summary: str = Field(description="Summary of relevant AAOIFI Shariah Standards")

class ShariahComplianceAgent:
    """Agent for checking Shariah compliance of bank rules against AAOIFI standards."""
    
    def __init__(self):
        """Initialize the Shariah Compliance Checker agent."""
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.system_prompt = """
You are a Shariah Compliance Checker Agent in an Islamic Finance advisory system.

Your task is to evaluate whether a given internal banking rule or product structure complies with AAOIFI Shariah Standards (SS). You will base your analysis **only** on the content retrieved from relevant SS documents.

You are provided with:
- rule_text: {rule_text}
- ss_summary: {ss_summary}

Your objective is to assess the **degree of Shariah compliance** of the rule_text and justify your decision clearly with reference to SS.

Your output must be a valid JSON object in the following format:

{
  "compliance_status": "compliant" | "partially_compliant" | "non_compliant",
  "justification": "string — explanation based on the SS summary",
  "referenced_clauses": [
    "string — quote or summarize key SS clauses that informed your decision"
  ]
}

Instructions:
- Be strict but fair: If the rule clearly contradicts or omits required Shariah principles, mark as "non_compliant".
- If it respects some requirements but misses or misapplies others, use "partially_compliant".
- If all key principles are met, mark it as "compliant".
- Base your assessment only on the SS summary provided; do not speculate beyond it.
- The justification must cite **specific Shariah principles or rules** as outlined in the summary.

Return only a clean JSON object as specified above.
"""

    def check_compliance(self, input_data: ComplianceInput) -> ComplianceResult:
        """
        Check a bank rule for compliance with AAOIFI Shariah Standards.
        
        Args:
            input_data: ComplianceInput object containing rule and SS summary
            
        Returns:
            ComplianceResult object containing compliance analysis
        """
        try:
            # Format the user message
            user_message = self._format_user_message(input_data)
            
            # Get analysis from OpenAI
            response = self.client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.2,
                response_format={"type": "json_object"}
            )
            
            # Parse the response
            analysis_data = response.choices[0].message.content
            # Try to parse as JSON first
            try:
                json_data = json.loads(analysis_data)
                return ComplianceResult.parse_obj(json_data)
            except json.JSONDecodeError:
                # If not valid JSON, try to parse as string
                return ComplianceResult.parse_raw(analysis_data)
            
        except Exception as e:
            print(f"Error during compliance check: {e}")
            raise

    def _format_user_message(self, input_data: ComplianceInput) -> str:
        """Format the input data into a structured message for the LLM."""
        return f"""
Rule Text:
{input_data.rule_text}

Shariah Standards Summary:
{input_data.ss_summary}
""" 