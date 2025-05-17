"""
Risk Analysis Agent
Purpose: Analyzes financial products and regulations for Shariah compliance and risk assessment.
"""

from typing import List, Dict, Optional, Union
from pydantic import BaseModel, Field
from openai import OpenAI
from ..core.config import settings
import json

class RiskAssessment(BaseModel):
    """Model for risk assessment results."""
    risk_name: str
    risk_type: str
    description: str
    shariah_implication: str
    mitigation_strategy: str
    severity: str = Field(default="Medium", description="Risk severity level")
    fas_reference: Optional[str] = Field(default=None, description="Relevant FAS standard reference")

class RiskAnalysisInput(BaseModel):
    """Input model for risk analysis."""
    product_description: str = Field(description="The product description or regulation clause.")
    standard: str = Field(description="The product type or reference standard (e.g., FAS_30).")
    known_risks: Optional[List[str]] = Field(default=None, description="Previously known risks associated with that standard.")

class RiskAnalysisResult(BaseModel):
    """Model for complete risk analysis results."""
    risks: List[RiskAssessment]
    summary: str
    fas_compliance_status: str
    recommendations: List[str]

class RiskAnalysisAgent:
    def __init__(self):
        """Initialize the Risk Analysis agent."""
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.system_prompt = """
You are a Risk Analysis Agent specialized in Islamic Finance and Shariah-compliant financial regulation mainly in AAOIFI standards.

Your task is to analyze a proposed financial regulation, policy, or product specification and identify the potential risks associated with it. Your risk analysis must be informed by Islamic finance principles, particularly the AAOIFI Financial Accounting Standards (FAS), as well as general financial risk knowledge.

You must distinguish between **general risks** (e.g., credit risk, operational risk, liquidity risk) and **Shariah-specific risks** (e.g., riba, gharar, prohibited contract structures, reputational risk due to non-compliance with FAS).

Return your analysis in a structured JSON format with the following fields for each risk:
- risk_name: Concise title of the risk
- risk_type: [Shariah | Operational | Financial | Reputational]
- description: Brief but precise explanation
- shariah_implication: Why it matters from a Shariah perspective
- mitigation_strategy: FAS-aligned advice or best practice
- severity: [High | Medium | Low]
- fas_reference: Relevant FAS standard reference (if applicable)

Also include:
- summary: Overall assessment summary
- fas_compliance_status: [Compliant | Partially Compliant | Non-Compliant]
- recommendations: List of key recommendations

IMPORTANT: Your response must be valid JSON that can be parsed by Python's json.loads() function.
"""

    def analyze_risk(self, input_data: RiskAnalysisInput) -> RiskAnalysisResult:
        """
        Analyze risks for a given financial product or regulation.
        
        Args:
            input_data: RiskAnalysisInput object containing product details
            
        Returns:
            RiskAnalysisResult object containing structured risk analysis
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
            analysis_data = response.choices[0].message.content.strip()
            
            # Try to parse as JSON first
            try:
                json_data = json.loads(analysis_data)
                return RiskAnalysisResult.parse_obj(json_data)
            except json.JSONDecodeError as json_err:
                print(f"JSON parsing error: {json_err}")
                print(f"Raw response: {analysis_data}")
                
                # Try to fix common JSON formatting issues
                try:
                    # Replace single quotes with double quotes
                    fixed_json = analysis_data.replace("'", '"')
                    json_data = json.loads(fixed_json)
                    return RiskAnalysisResult.parse_obj(json_data)
                except:
                    # If all parsing attempts fail, create a basic result
                    return RiskAnalysisResult(
                        risks=[RiskAssessment(
                            risk_name="Parsing Error",
                            risk_type="Operational",
                            description="Failed to parse risk analysis response",
                            shariah_implication="Unable to assess Shariah implications",
                            mitigation_strategy="Review and fix the risk analysis response format",
                            severity="High"
                        )],
                        summary="Error in risk analysis",
                        fas_compliance_status="Unknown",
                        recommendations=["Fix the risk analysis response format"]
                    )
            
        except Exception as e:
            print(f"Error during risk analysis: {e}")
            raise

    def _format_user_message(self, input_data: RiskAnalysisInput) -> str:
        """Format the input data into a structured message for the LLM."""
        message_parts = [
            "Product Description:",
            input_data.product_description,
            "\nStandard:",
            input_data.standard
        ]
        
        if input_data.known_risks:
            message_parts.append("\nKnown Risks:")
            message_parts.extend(input_data.known_risks)
        
        return "\n".join(message_parts)

    def get_available_standards(self) -> List[str]:
        """Return list of available FAS standards for risk analysis."""
        return [
            "FAS_4_Musharaka",
            "FAS_7_Salam_Parallel_Salam",
            "FAS_10_Istisna",
            "FAS_28_Murabaha_Deferred_Payment_Sales",
            "FAS_32_Ijarah",
            "FAS_30_Investment_Accounts"
        ]

