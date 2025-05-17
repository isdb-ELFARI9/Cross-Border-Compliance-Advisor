"""
Compliance Scanner Agent
Purpose: Scans regulation drafts for compliance issues using the ShariahComplianceAgent.
"""

from typing import Dict, List, Any
from pydantic import BaseModel, Field
from openai import OpenAI
from ...core.config import settings
from ...agents.shariah_compliance_agent import ShariahComplianceAgent, ComplianceInput
import json

class ProblematicField(BaseModel):
    """Model for a problematic field in the regulation draft."""
    location: str = Field(description="Location of the field in the regulation structure")
    text: str = Field(description="The problematic text content")
    compliance_status: str = Field(
        description="Compliance status: compliant, partially_compliant, or non_compliant",
        pattern="^(compliant|partially_compliant|non_compliant)$"
    )
    justification: str = Field(description="Explanation of the compliance issue")
    referenced_clauses: List[str] = Field(
        default_factory=list,
        description="List of referenced Shariah Standard clauses"
    )

class ComplianceScanResult(BaseModel):
    """Model for the complete compliance scan result."""
    problematic_fields: List[ProblematicField] = Field(
        default_factory=list,
        description="List of fields with compliance issues"
    )

class DraftRegulation(BaseModel):
    """Model for the regulation draft structure."""
    external_regulation: List[Dict[str, str]] = Field(description="External regulation sections")
    internal_rulebook: List[Dict[str, str]] = Field(description="Internal rulebook sections")

class ComplianceScannerAgent:
    """Agent for scanning regulation drafts for compliance issues."""
    
    def __init__(self):
        """Initialize the Compliance Scanner agent."""
        self.compliance_agent = ShariahComplianceAgent()
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        
    def scan_draft(self, draft_regulation: List[Dict[str, List[Dict[str, str]]]]) -> ComplianceScanResult:
        """
        Scan a regulation draft for compliance issues.
        
        Args:
            draft_regulation: List of dictionaries containing the regulation draft structure
            
        Returns:
            ComplianceScanResult object containing all problematic fields
        """
        try:
            problematic_fields = []
            
            # Process each section in the draft regulation
            for section in draft_regulation:
                # Process External Regulation sections
                for external_section in section.get("External Regulation", []):
                    for section_name, content in external_section.items():
                        # Check compliance for this section
                        compliance_result = self._check_section_compliance(
                            content,
                            f"External Regulation > {section_name}"
                        )
                        
                        # Add to problematic fields if not fully compliant
                        if compliance_result.compliance_status != "compliant":
                            problematic_fields.append(
                                ProblematicField(
                                    location=f"External Regulation > {section_name}",
                                    text=content,
                                    compliance_status=compliance_result.compliance_status,
                                    justification=compliance_result.justification,
                                    referenced_clauses=compliance_result.referenced_clauses
                                )
                            )
                
                # Process Internal Rulebook sections
                for internal_section in section.get("Internal Rulebook", []):
                    for section_name, content in internal_section.items():
                        # Check compliance for this section
                        compliance_result = self._check_section_compliance(
                            content,
                            f"Internal Rulebook > {section_name}"
                        )
                        
                        # Add to problematic fields if not fully compliant
                        if compliance_result.compliance_status != "compliant":
                            problematic_fields.append(
                                ProblematicField(
                                    location=f"Internal Rulebook > {section_name}",
                                    text=content,
                                    compliance_status=compliance_result.compliance_status,
                                    justification=compliance_result.justification,
                                    referenced_clauses=compliance_result.referenced_clauses
                                )
                            )
            
            return ComplianceScanResult(problematic_fields=problematic_fields)
            
        except Exception as e:
            print(f"Error scanning regulation draft: {e}")
            raise

    def _check_section_compliance(self, content: str, section_name: str) -> Any:
        """
        Check compliance for a single section using the ShariahComplianceAgent.
        
        Args:
            content: The section content to check
            section_name: Name of the section being checked
            
        Returns:
            ComplianceResult from the ShariahComplianceAgent
        """
        try:
            # TODO: In a real implementation, you would need to provide relevant SS summary
            # For now, using a placeholder SS summary
            
            # Create input for compliance check
            compliance_input = ComplianceInput(
                rule_text=content,
                ss_summary=""
            )
            
            # Get compliance result
            return self.compliance_agent.check_compliance(compliance_input)
            
        except Exception as e:
            print(f"Error checking section compliance: {e}")
            raise
