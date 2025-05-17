"""
Ambiguity Detection Agent
Purpose: Analyzes bank rules and policies for ambiguous language against AAOIFI standards.
"""

from typing import List, Optional
from pydantic import BaseModel, Field
from openai import OpenAI
from ..core.config import settings
import json

class AmbiguousElement(BaseModel):
    """Model for ambiguous element analysis."""
    text: str = Field(description="The specific clause or phrase that is ambiguous")
    reason: str = Field(description="Why this element is ambiguous in a FAS/SS context")
    required_clarification: str = Field(description="What clarification is needed to comply with AAOIFI standards")

class AmbiguityAnalysisInput(BaseModel):
    """Input model for ambiguity analysis."""
    rule_text: str = Field(description="The bank's internal rule or policy to analyze")
    fas_summary: str = Field(description="Summary of relevant AAOIFI FAS")
    ss_summary: str = Field(description="Summary of relevant Shariah Standards")

class AmbiguityAnalysisResult(BaseModel):
    """Model for ambiguity analysis results."""
    ambiguous: bool = Field(description="Whether ambiguity exists")
    ambiguous_elements: List[AmbiguousElement] = Field(default_factory=list, description="List of identified ambiguities")

class AmbiguityDetectionAgent:
    """Agent for detecting ambiguities in bank rules against AAOIFI standards."""
    
    def __init__(self):
        """Initialize the Ambiguity Detection agent."""
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.system_prompt = """
You are an Ambiguity Detection Agent for an Islamic Financial Compliance Advisor.  
Your role is to review a bank's internal rule or policy and determine whether it contains ambiguous, vague, or underspecified language, especially in light of:

- AAOIFI Financial Accounting Standards (FAS)  
- AAOIFI Shariah Standards (SS)

Your goal is to ensure that each rule is clear, specific, and aligned with the interpretive expectations of FAS and SS.

You are given:
- rule_text: {rule_text}
- fas_summary: {fas_summary}
- ss_summary: {ss_summary}

Your response must be a valid JSON object with the following structure:

{
  "ambiguous": true | false,
  "ambiguous_elements": [
    {
      "text": "string — the specific clause or phrase that is ambiguous",
      "reason": "string — why this element is ambiguous in a FAS/SS context",
      "required_clarification": "string — what clarification or precision is needed to comply with AAOIFI standards"
    }
  ]
}

Instructions:
- Set "ambiguous": false if the rule is fully clear and no ambiguity exists; leave other fields empty ([]).
- Otherwise, identify each vague clause, explain why it's problematic, and suggest the kind of clarification or specification that would resolve it.
- Focus on ambiguities from the perspective of Islamic finance — i.e., anything that can cause non-compliance with FAS or Shariah due to vague interpretation.
- Be especially sensitive to:
  - Undefined terms (e.g., "fee", "return", "margin")
  - Lack of contract structure or transaction type
  - Non-specific roles, conditions, or timelines

Example Judgments:
- A rule says "profit will be distributed fairly" → ambiguous: what does "fairly" mean under FAS?
- A policy references "interest or return" → ambiguous or possibly conflicting term
- Clause allows "discretionary modification" of pricing → ambiguous in contractual certainty context

Always output strict, valid JSON, and make sure explanations are short but clear.
"""

    def analyze_ambiguity(self, input_data: AmbiguityAnalysisInput) -> AmbiguityAnalysisResult:
        """
        Analyze a bank rule for ambiguities against AAOIFI standards.
        
        Args:
            input_data: AmbiguityAnalysisInput object containing rule and standard summaries
            
        Returns:
            AmbiguityAnalysisResult object containing ambiguity analysis
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
                return AmbiguityAnalysisResult.parse_obj(json_data)
            except json.JSONDecodeError:
                # If not valid JSON, try to parse as string
                return AmbiguityAnalysisResult.parse_raw(analysis_data)
            
        except Exception as e:
            print(f"Error during ambiguity analysis: {e}")
            raise

    def _format_user_message(self, input_data: AmbiguityAnalysisInput) -> str:
        """Format the input data into a structured message for the LLM."""
        return f"""
Rule Text:
{input_data.rule_text}

FAS Summary:
{input_data.fas_summary}

Shariah Standards Summary:
{input_data.ss_summary}
""" 