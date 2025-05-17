"""
Update Advisor Agent
Purpose: Proposes Shariah-compliant updates to non-compliant regulations based on AAOIFI standards.
"""

from typing import List, Optional
from pydantic import BaseModel, Field
from openai import OpenAI
from ..core.config import settings
import json

class UpdateProposal(BaseModel):
    """Model for update proposal results."""
    proposed_update: str = Field(description="The revised, fully Shariah-compliant clause or policy")
    rationale: str = Field(description="Concise justification citing specific SS clauses")

class UpdateInput(BaseModel):
    """Input model for update analysis."""
    non_compliant_text: str = Field(description="The original clause or policy text that violates Shariah standards")
    issue_summary: str = Field(description="Brief explanation of the non-compliance")
    context_type: str = Field(description="Regulatory domain (e.g., 'Accounting Standards', 'Risk Management')")
    ss_documents: List[str] = Field(description="List of relevant AAOIFI SS excerpts to guide the update")

class UpdateAdvisorAgent:
    """Agent for proposing Shariah-compliant updates to non-compliant regulations."""
    
    def __init__(self):
        """Initialize the Update Advisor agent."""
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.system_prompt = """
You are the **UpdateAdvisorAgent**, an expert in drafting Shariah-compliant regulatory updates according to AAOIFI Shariah Standards (SS).

## Objective
Revise a regulation clause that has been flagged as non-compliant and propose a Shariah-compliant alternative, strictly based on the provided SS excerpts.

## Input
You receive a JSON object with the following fields:
{
  "non_compliant_text": "{non_compliant_text}",
  "issue_summary": "{issue_summary}",
  "context_type": "{context_type}",
  "ss_documents": {ss_documents}
}

- **non_compliant_text**: The original clause or policy text that violates Shariah standards.
- **issue_summary**: Brief explanation of the non-compliance.
- **context_type**: Regulatory domain (e.g., "Accounting Standards", "Risk Management").
- **ss_documents**: A JSON array of relevant AAOIFI SS excerpts to guide your update.

## Output
Return **only** a valid JSON object in the following format:

{
  "proposed_update": "string — the revised, fully Shariah-compliant clause or policy",
  "rationale": "string — concise justification citing specific SS clauses"
}

## Guidelines
1. Base your recommendation on the provided SS excerpts , the shariah standard and the issue summary.
2. Ensure the proposed text is clear, precise, and legally meaningful.
3. In the **rationale**, explicitly reference SS document numbers or clauses (e.g., "SS No. 3: Late penalties…").
4. If no compliant alternative is possible, return:

{
  "proposed_update": "",
  "rationale": "No compliant alternative possible because …"
}

5. Do **not** return any extra text, commentary, or keys—only the JSON object above.
"""

    def propose_update(self, input_data: UpdateInput) -> UpdateProposal:
        """
        Propose a Shariah-compliant update to a non-compliant regulation.
        
        Args:
            input_data: UpdateInput object containing non-compliant text and context
            
        Returns:
            UpdateProposal object containing the proposed update and rationale
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
                return UpdateProposal.parse_obj(json_data)
            except json.JSONDecodeError:
                # If not valid JSON, try to parse as string
                return UpdateProposal.parse_raw(analysis_data)
            
        except Exception as e:
            print(f"Error during update proposal: {e}")
            raise

    def _format_user_message(self, input_data: UpdateInput) -> str:
        """Format the input data into a structured message for the LLM."""
        return f"""
Non-compliant Text:
{input_data.non_compliant_text}

Issue Summary:
{input_data.issue_summary}

Context Type:
{input_data.context_type}

SS Documents:
{json.dumps(input_data.ss_documents, indent=2)}
""" 