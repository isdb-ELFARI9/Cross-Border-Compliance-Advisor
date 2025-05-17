"""
Test script for the UpdateAdvisorAgent.
"""

import sys
import os

# Add the src directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.agents.update_advisor_agent import (
    UpdateAdvisorAgent,
    UpdateInput
)

def main():
    """Test update proposal with a non-compliant Murabaha contract clause."""
    # Create agent instance
    agent = UpdateAdvisorAgent()
    
    # Create test input
    input_data = UpdateInput(
        non_compliant_text="""
        Late payment fees will be charged at 2% per month on the outstanding balance.
        The fees will be added to the customer's debt amount.
        """,
        issue_summary="The clause violates Shariah principles by increasing debt through late payment fees",
        context_type="Murabaha Contract Terms",
        ss_documents=[
            """
            SS No. 1 (Murabaha):
            - Late payment penalties must not increase the debt amount
            - Penalties should be treated as charitable contributions
            - The bank must not benefit from late payment penalties
            """,
            """
            SS No. 3 (Penalties):
            - Penalties must be used for charitable purposes
            - No direct benefit to the bank from penalties
            - Clear disclosure of penalty treatment required
            """
        ]
    )
    
    try:
        # Get analysis result
        result = agent.propose_update(input_data)
        
        # Print the analysis result
        print("\n=== Update Proposal Results ===")
        print(f"\nProposed Update:")
        print(result.proposed_update)
        print(f"\nRationale:")
        print(result.rationale)
            
    except Exception as e:
        print(f"Error during analysis: {e}")

if __name__ == "__main__":
    main() 