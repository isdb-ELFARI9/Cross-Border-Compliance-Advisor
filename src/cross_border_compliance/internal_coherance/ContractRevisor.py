"""
Contract Revisor Agent
Purpose: Revises contract sections to resolve regulatory and legal conflicts, ensuring clarity and compliance.
"""

from typing import Optional
from pydantic import BaseModel, Field
from openai import OpenAI
from ...core.config import settings

class RevisionInput(BaseModel):
    section_name: str = Field(description="Name of the contract section")
    original_content: str = Field(description="Original content of the section")
    conflict_description: str = Field(description="Description of the conflict")
    recommendation: str = Field(description="Recommended resolution approach")

class RevisionResult(BaseModel):
    revised_content: str = Field(description="Revised contract section content")
    rationale: Optional[str] = Field(default=None, description="Rationale for the revision")

class ContractRevisor:
    """Agent for revising contract sections to resolve regulatory and legal conflicts."""
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.system_prompt = (
            """
You are a Contract Revision Agent specializing in cross-border financial and regulatory contracts.

Your task is to revise contract sections to resolve conflicts between different regulatory frameworks by complying primarily with AAOIFI (Accounting and Auditing Organization for Islamic Financial Institutions) standards.

Guidelines:

- Revise the section to address the described conflict by ensuring alignment with AAOIFI standards.
Where other frameworks (e.g., IFRS, EU law) conflict with AAOIFI, prioritize AAOIFI compliance while maintaining legal and financial clarity.
- Do not remove important legal or financial details unless they directly contradict AAOIFI principles.
- If the recommendation is ambiguous, revise the section to clarify the intent in line with AAOIFI requirements.
- Return only the revised section text, not the entire contract.
- Optionally, provide a brief rationale for your revision.

Format your response as JSON:
{
  "revised_content": "...",
  "rationale": "..." // optional
}
"""
        )

    def revise_section(self, input_data: RevisionInput) -> RevisionResult:
        """
        Revise a contract section to resolve a conflict.
        Args:
            input_data: RevisionInput object
        Returns:
            RevisionResult object
        """
        user_message = self._format_user_message(input_data)
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.2,
            response_format={"type": "json_object"}
        )
        content = response.choices[0].message.content
        import json
        data = json.loads(content)
        return RevisionResult(**data)

    def _format_user_message(self, input_data: RevisionInput) -> str:
        return f"""
Section Name: {input_data.section_name}
Original Content:
{input_data.original_content}

Conflict Description:
{input_data.conflict_description}

Recommendation:
{input_data.recommendation}
""" 