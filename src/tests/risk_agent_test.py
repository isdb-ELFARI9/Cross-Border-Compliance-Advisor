"""
Test suite for the RiskAnalysisAgent class.
"""

import sys
import os
from typing import List

# Add the src directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import pytest
from unittest.mock import Mock, patch
from src.agents.risk_agent import (
    RiskAnalysisAgent,
    RiskAnalysisInput,
    RiskAnalysisResult,
    RiskAssessment
)



# Sample test data
SAMPLE_PRODUCT_DESCRIPTION = """
A Murabaha contract for financing the purchase of a vehicle. The Islamic bank 
purchases the vehicle from the dealer and sells it to the customer at a cost-plus-profit margin. 
The selling price is fixed at the time of contract and paid in installments.
"""

SAMPLE_KNOWN_RISKS = ["Credit risk", "Market risk"]

# Mock response data
MOCK_ANALYSIS_RESPONSE = {
    "risks": [
        {
            "risk_name": "Credit Risk",
            "risk_type": "Financial",
            "description": "Risk of customer default on payments",
            "shariah_implication": "Must ensure proper risk sharing",
            "mitigation_strategy": "Implement proper credit assessment",
            "severity": "High",
            "fas_reference": "FAS_28"
        },
        {
            "risk_name": "Market Risk",
            "risk_type": "Operational",
            "description": "Risk of market value fluctuations",
            "shariah_implication": "Must avoid gharar",
            "mitigation_strategy": "Use conservative pricing",
            "severity": "Medium",
            "fas_reference": "FAS_28"
        }
    ],
    "summary": "Overall compliant with minor risks",
    "fas_compliance_status": "Compliant",
    "recommendations": [
        "Implement strict credit assessment",
        "Use conservative pricing models"
    ]
}

@pytest.fixture
def risk_agent():
    """Fixture to create a RiskAnalysisAgent instance."""
    with patch('openai.OpenAI') as mock_openai:
        agent = RiskAnalysisAgent()
        yield agent

@pytest.fixture
def mock_openai_response():
    """Fixture to create a mock OpenAI response."""
    mock_response = Mock()
    mock_response.choices = [
        Mock(
            message=Mock(
                content=str(MOCK_ANALYSIS_RESPONSE)
            )
        )
    ]
    return mock_response

def test_risk_agent_initialization(risk_agent):
    """Test proper initialization of RiskAnalysisAgent."""
    assert risk_agent is not None
    assert hasattr(risk_agent, 'client')
    assert hasattr(risk_agent, 'system_prompt')

def test_format_user_message(risk_agent):
    """Test the _format_user_message method."""
    input_data = RiskAnalysisInput(
        product_description=SAMPLE_PRODUCT_DESCRIPTION,
        standard="FAS_28",
        known_risks=SAMPLE_KNOWN_RISKS
    )
    
    message = risk_agent._format_user_message(input_data)
    
    assert "Product Description:" in message
    assert SAMPLE_PRODUCT_DESCRIPTION in message
    assert "Standard:" in message
    assert "FAS_28" in message
    assert "Known Risks:" in message
    for risk in SAMPLE_KNOWN_RISKS:
        assert risk in message

def test_analyze_risk_success(risk_agent, mock_openai_response):
    """Test successful risk analysis."""
    # Setup mock
    risk_agent.client.chat.completions.create.return_value = mock_openai_response
    
    input_data = RiskAnalysisInput(
        product_description=SAMPLE_PRODUCT_DESCRIPTION,
        standard="FAS_28",
        known_risks=SAMPLE_KNOWN_RISKS
    )
    
    result = risk_agent.analyze_risk(input_data)
    
    # Verify the result structure
    assert isinstance(result, RiskAnalysisResult)
    assert len(result.risks) == 2
    assert result.fas_compliance_status == "Compliant"
    assert len(result.recommendations) == 2
    
    # Verify the risk details
    risk = result.risks[0]
    assert isinstance(risk, RiskAssessment)
    assert risk.risk_name == "Credit Risk"
    assert risk.risk_type == "Financial"
    assert risk.severity == "High"

def test_analyze_risk_error(risk_agent):
    """Test error handling in risk analysis."""
    # Setup mock to raise an exception
    risk_agent.client.chat.completions.create.side_effect = Exception("API Error")
    
    input_data = RiskAnalysisInput(
        product_description=SAMPLE_PRODUCT_DESCRIPTION,
        standard="FAS_28",
        known_risks=SAMPLE_KNOWN_RISKS
    )
    
    with pytest.raises(Exception) as exc_info:
        risk_agent.analyze_risk(input_data)
    
    assert "Error during risk analysis" in str(exc_info.value)

def test_get_available_standards(risk_agent):
    """Test the get_available_standards method."""
    standards = risk_agent.get_available_standards()
    
    assert isinstance(standards, list)
    assert len(standards) > 0
    assert "FAS_28_Murabaha_Deferred_Payment_Sales" in standards
    assert "FAS_32_Ijarah" in standards

def test_risk_analysis_input_validation():
    """Test RiskAnalysisInput validation."""
    # Test valid input
    valid_input = RiskAnalysisInput(
        product_description=SAMPLE_PRODUCT_DESCRIPTION,
        standard="FAS_28"
    )
    assert valid_input.product_description == SAMPLE_PRODUCT_DESCRIPTION
    assert valid_input.standard == "FAS_28"
    assert valid_input.known_risks is None
    
    # Test with known risks
    input_with_risks = RiskAnalysisInput(
        product_description=SAMPLE_PRODUCT_DESCRIPTION,
        standard="FAS_28",
        known_risks=SAMPLE_KNOWN_RISKS
    )
    assert input_with_risks.known_risks == SAMPLE_KNOWN_RISKS

def test_risk_assessment_validation():
    """Test RiskAssessment validation."""
    risk = RiskAssessment(
        risk_name="Test Risk",
        risk_type="Financial",
        description="Test Description",
        shariah_implication="Test Implication",
        mitigation_strategy="Test Strategy",
        severity="High",
        fas_reference="FAS_28"
    )
    
    assert risk.risk_name == "Test Risk"
    assert risk.risk_type == "Financial"
    assert risk.severity == "High"
    assert risk.fas_reference == "FAS_28"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
