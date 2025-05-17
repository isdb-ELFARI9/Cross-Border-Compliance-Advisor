"""
Conflict Detection Agent
Purpose: Analyzes bank rules and practices for conflicts with AAOIFI FAS and Shariah Standards.
"""

from typing import List, Dict, Optional
from pydantic import BaseModel, Field
from openai import OpenAI
from ..core.config import settings
import json

class ConflictElement(BaseModel):
    """Model for individual conflict elements."""
    bank_element: str = Field(description="The problematic term or practice in the rule or contract")
    fas_conflict: str = Field(description="How it contradicts AAOIFI FAS")
    ss_conflict: str = Field(description="How it contradicts Shariah standards")

class ConflictAnalysisInput(BaseModel):
    """Input model for conflict analysis."""
    rule_text: str = Field(description="The bank's internal rule or practice to analyze")
    fas_summary: str = Field(description="Summary of relevant AAOIFI FAS")
    ss_summary: str = Field(description="Summary of relevant Shariah Standards")

class ConflictAnalysisResult(BaseModel):
    """Model for conflict analysis results."""
    conflict: bool = Field(description="Whether a conflict exists")
    conflicting_elements: List[ConflictElement] = Field(default_factory=list, description="List of identified conflicts")
    justification: str = Field(default="", description="Explanation of conflicts")
    references: List[str] = Field(default_factory=list, description="References to FAS and SS standards")

class ConflictDetectionAgent:
    def __init__(self):
        """Initialize the Conflict Detection agent."""
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.system_prompt = """
You are a Conflict Detection Agent specializing in Islamic financial compliance.
Your task is to analyze a bank's internal rule or practice and identify any conflicts with:

* AAOIFI Financial Accounting Standards (FAS)
* AAOIFI Shariah Standards (SS)

You are given:
* A rule from the bank: {rule_text}
* Relevant FAS summary: {fas_summary}
* Relevant Shariah Standards summary: {ss_summary}

Your response must be a valid JSON object with the following structure:
{
  "conflict": true | false,
  "conflicting_elements": [
    {
      "bank_element": "string — the problematic term or practice in the rule",
      "fas_conflict": "string — how it contradicts AAOIFI FAS",
      "ss_conflict": "string — how it contradicts Shariah standards"
    }
  ],
  "justification": "string — concise explanation referencing both FAS and SS",
  "references": [
    "string — e.g., 'FAS 28 para 5'", 
    "string — e.g., 'Shariah Standard No. 8'"
  ]
}

Guidelines:
* Be specific in identifying conflicts
* If no conflict exists, set "conflict": false and leave other fields empty ([] or "")
* Output must always be valid JSON
* Justify based on both FAS and SS principles
* Always reason from a Shariah-compliant perspective, and prioritize AAOIFI guidance over conventional views
* Be concise but clear and authoritative

IMPORTANT: Your response must be valid JSON that can be parsed by Python's json.loads() function.
"""

    def analyze_conflict(self, input_data: ConflictAnalysisInput) -> ConflictAnalysisResult:
        """
        Analyze a bank rule for conflicts with AAOIFI standards.
        
        Args:
            input_data: ConflictAnalysisInput object containing rule and standard summaries
            
        Returns:
            ConflictAnalysisResult object containing conflict analysis
        """
        try:
            # Format the user message
            user_message = self._format_user_message(input_data)
            
            # Get analysis from OpenAI
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",  # or your preferred model
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.2
            )
            
            # Parse the response
            analysis_data = response.choices[0].message.content
            # Try to parse as JSON first
            try:
                json_data = json.loads(analysis_data)
                return ConflictAnalysisResult.parse_obj(json_data)
            except json.JSONDecodeError:
                # If not valid JSON, try to parse as string
                return ConflictAnalysisResult.parse_raw(analysis_data)
            
        except Exception as e:
            print(f"Error during conflict analysis: {e}")
            raise

    def _format_user_message(self, input_data: ConflictAnalysisInput) -> str:
        """Format the input data into a structured message for the LLM."""
        return f"""
Rule Text:
{input_data.rule_text}

FAS Summary:
{input_data.fas_summary}

Shariah Standards Summary:
{input_data.ss_summary}
"""

    def get_available_standards(self) -> List[str]:
        """Return list of available FAS and Shariah Standards for conflict analysis."""
        return [
            "FAS_4_Musharaka",
            "FAS_7_Salam_Parallel_Salam",
            "FAS_10_Istisna",
            "FAS_28_Murabaha_Deferred_Payment_Sales",
            "FAS_32_Ijarah",
            "FAS_30_Investment_Accounts",
            "SS_1_Murabaha",
            "SS_2_Salam",
            "SS_3_Istisna",
            "SS_4_Ijarah"
        ]
