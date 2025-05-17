"""
Gap Detection Agent
Purpose: Analyzes bank rules and policies for missing elements required by AAOIFI standards.
"""

from typing import List, Optional
from pydantic import BaseModel, Field
from openai import OpenAI
from ..core.config import settings
import json

class MissingElement(BaseModel):
    """Model for missing element analysis."""
    requirement: str = Field(description="A requirement from FAS or SS that is not found in the rule")
    importance: str = Field(description="Why this requirement is necessary from a Shariah/FAS compliance perspective")
    recommendation: str = Field(description="How to amend or extend the rule to include the missing element")

class GapAnalysisInput(BaseModel):
    """Input model for gap analysis."""
    rule_text: str = Field(description="The bank's internal rule or policy to analyze")
    fas_summary: str = Field(description="Summary of relevant AAOIFI FAS")
    ss_summary: str = Field(description="Summary of relevant Shariah Standards")

class GapAnalysisResult(BaseModel):
    """Model for gap analysis results."""
    has_gaps: bool = Field(description="Whether any required elements are missing")
    missing_elements: List[MissingElement] = Field(default_factory=list, description="List of identified missing elements")

class GapDetectionAgent:
    """Agent for detecting gaps in bank rules against AAOIFI standards."""
    
    def __init__(self):
        """Initialize the Gap Detection agent."""
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.system_prompt = """
You are a Gap Detection Agent in an Islamic Financial Compliance System.

Your role is to analyze a given internal banking rule or product specification and detect any **missing elements** that are **required** by AAOIFI Financial Accounting Standards (FAS) and AAOIFI Shariah Standards (SS). Your objective is to ensure the rule fully addresses all necessary Shariah and accounting requirements.

You are provided with:
- rule_text: {rule_text}
- fas_summary: {fas_summary}
- ss_summary: {ss_summary}

Your output must be a valid JSON object in the following format:

{
  "has_gaps": true | false,
  "missing_elements": [
    {
      "requirement": "string — a requirement from FAS or SS that is not found in the rule_text",
      "importance": "string — why this requirement is necessary from a Shariah/FAS compliance perspective",
      "recommendation": "string — how to amend or extend the rule to include the missing element"
    }
  ]
}

Instructions:
- If all required elements are present, return `"has_gaps": false` and an empty list.
- If any essential requirement is not clearly addressed in the rule, set `"has_gaps": true` and populate the `missing_elements` array.
- Focus on:
  - Contractual components mandated by FAS (e.g. pricing terms, risk-sharing clauses)
  - Shariah-mandated conditions (e.g. avoidance of riba, gharar, or unjust enrichment)
  - Process-related gaps (e.g. missing governance or disclosure steps)

Be concise but precise in your justifications. Ensure your JSON is clean, valid, and interpretable by a compliance processing system.
"""

    def analyze_gaps(self, input_data: GapAnalysisInput) -> GapAnalysisResult:
        """
        Analyze a bank rule for missing elements required by AAOIFI standards.
        
        Args:
            input_data: GapAnalysisInput object containing rule and standard summaries
            
        Returns:
            GapAnalysisResult object containing gap analysis
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
            # Try to parse as JSON first
            try:
                json_data = json.loads(analysis_data)
                return GapAnalysisResult.parse_obj(json_data)
            except json.JSONDecodeError:
                # If not valid JSON, try to parse as string
                return GapAnalysisResult.parse_raw(analysis_data)
            
        except Exception as e:
            print(f"Error during gap analysis: {e}")
            raise

    def _format_user_message(self, input_data: GapAnalysisInput) -> str:
        """Format the input data into a structured message for the LLM."""
        return f"""
Rule Text:
{input_data.rule_text}

FAS Summary:
{input_data.fas_summary}

Shariah Standards Summary:
{input_data.ss_summary}
""" 