"""
Relevant Regulation Sections Identifier Agent
Purpose: Identifies which parts of the regulation framework are relevant to a given user query.
"""

from typing import Dict, List
from pydantic import BaseModel, Field
from openai import OpenAI
from src.core.config import settings
import json

class RegulationSections(BaseModel):
    """Model for identified regulation sections."""
    external_regulation: List[str] = Field(
        default_factory=list,
        description="List of relevant external regulation sections"
    )
    internal_rulebook: List[str] = Field(
        default_factory=list,
        description="List of relevant internal rulebook sections"
    )

class QueryInput(BaseModel):
    """Input model for query analysis."""
    query: str = Field(description="The user's query to analyze")

class RelevantRegulationSectionsIdentifier:
    """Agent for identifying relevant regulation sections based on user queries."""
    
    def __init__(self):
        """Initialize the Relevant Regulation Sections Identifier agent."""
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.system_prompt = """
You are an expert regulatory analyst.

Given a user query and a regulation document with known structured sections under "External Regulation" and "Internal Rulebook", your task is to identify which specific sections are most relevant to answering the query.

Respond in a compact JSON format like this:
{
  "External Regulation": ["<relevant_section_1>", ...],
  "Internal Rulebook": ["<relevant_section_2>", ...]
}

Only include the sections that are directly relevant to answering the query.

Available External Regulation sections:
- Capital Adequacy & Risk Management
- Liquidity Rules & Funding
- AntiMoney Laundering AML and Know Your Customer KYC
- Accounting Standards
- Legal Permissions & Product Approval

Available Internal Rulebook sections:
- Governance Policies
- Risk Management Framework
- Product Manuals
- Financial Policies
- Compliance & Ethics

Guidelines:
1. Be precise in matching query intent to relevant sections
2. Only include sections that are directly relevant
3. Consider both explicit and implicit connections
4. Return empty lists if no sections are relevant
5. Maintain the exact section names as provided
"""

    def identify_sections(self, input_data: QueryInput) -> RegulationSections:
        """
        Identify relevant regulation sections for a given query.
        
        Args:
            input_data: QueryInput object containing the user query
            
        Returns:
            RegulationSections object containing relevant sections
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
                return RegulationSections(
                    external_regulation=json_data.get("External Regulation", []),
                    internal_rulebook=json_data.get("Internal Rulebook", [])
                )
            except json.JSONDecodeError:
                # If not valid JSON, try to parse as string
                return RegulationSections.parse_raw(analysis_data)
            
        except Exception as e:
            print(f"Error identifying regulation sections: {e}")
            raise

    def _format_user_message(self, input_data: QueryInput) -> str:
        """Format the input data into a structured message for the LLM."""
        return f"""
Query: {input_data.query}
""" 