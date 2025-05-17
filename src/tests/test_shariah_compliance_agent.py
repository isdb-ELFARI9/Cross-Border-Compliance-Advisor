"""
Test script for the ShariahComplianceAgent.
"""

import sys
import os

# Add the src directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.agents.shariah_compliance_agent import (
    ShariahComplianceAgent,
    ComplianceInput
)

def main():
    """Test Shariah compliance check with a simple Murabaha contract rule."""
    # Create agent instance
    agent = ShariahComplianceAgent()
    
    # Create test input
    input_data = ComplianceInput(
        rule_text="""
        The bank will purchase goods from the supplier and sell them to the customer at a markup.
        The customer will pay in monthly installments over 12 months.
        Late payment fees will be charged at 2% per month.
        The bank reserves the right to modify the contract terms at any time.
        """,
        ss_summary="""
        Shariah Standard No. 1 (Murabaha) requires:
        - Complete asset specifications and ownership transfer
        - Clear pricing mechanism with fixed markup
        - No penalty fees that increase debt
        - No unilateral modification of contract terms
        - Proper disclosure of all terms
        - Risk transfer conditions must be clearly specified
        """
    )
    
    try:
        # Get analysis result
        result = agent.check_compliance(input_data)
        
        # Print the analysis result
        print("\n=== Shariah Compliance Analysis Results ===")
        print(f"\nCompliance Status: {result.compliance_status}")
        print(f"\nJustification: {result.justification}")
        
        if result.referenced_clauses:
            print("\nReferenced Clauses:")
            for clause in result.referenced_clauses:
                print(f"- {clause}")
            
    except Exception as e:
        print(f"Error during analysis: {e}")

if __name__ == "__main__":
    main() 