"""
Simple test script for ContractRevisor
"""

import sys
import os

# Add the src directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from src.cross_border_compliance.internal_coherance.ContractRevisor import (
    ContractRevisor,
    RevisionInput
)

def test_contract_revisor():
    print("\n=== Testing ContractRevisor ===\n")
    revisor = ContractRevisor()
    
    # Example input
    input_data = RevisionInput(
        section_name="Terms of Funding",
        original_content="- Provider shall make available €10,000,000 for a period of 6 months.\n- Recipient shall repay principal and an agreed return.",
        conflict_description="The contract does not specify the nature of the 'agreed return' on the funding.",
        recommendation="Specify the agreed return as a fixed interest rate, profit share ratio, or any other mutually agreed upon method to ensure clarity and alignment between parties."
    )
    print("Requesting revision from LLM...")
    result = revisor.revise_section(input_data)
    print("\nRevised Content:\n", result.revised_content)
    if result.rationale:
        print("\nRationale:\n", result.rationale)
    print("\n=== Test Completed ===\n")

if __name__ == "__main__":
    test_contract_revisor() 