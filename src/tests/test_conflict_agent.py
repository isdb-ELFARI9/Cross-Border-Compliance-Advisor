
import sys
import os
from typing import List

# Add the src directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.agents.conflict_agent import (
    ConflictDetectionAgent,
    ConflictAnalysisInput,
    ConflictAnalysisResult,
    ConflictElement
)

def test_conflict_analysis():
    """Test conflict analysis with a simple Murabaha contract rule."""
    # Create agent instance
    agent = ConflictDetectionAgent()
    
    # Create test input
    input_data = ConflictAnalysisInput(
        rule_text="""
        The bank charges a fixed penalty of 2% per month on late payments for Murabaha contracts.
        The penalty is added to the customer's outstanding balance.
        """,
        fas_summary="""
        FAS 28 (Murabaha) prohibits charging penalties that increase the debt amount.
        Penalties should be treated as charitable contributions.
        """,
        ss_summary="""
        Shariah Standard No. 1 (Murabaha) prohibits increasing the debt amount through penalties.
        Penalties must be treated as charitable contributions to be used for charitable purposes.
        """
    )
    
    # Get analysis result
    result = agent.analyze_conflict(input_data)
    
    # Print the analysis result
    print("\nConflict Analysis Result:")
    print(f"Conflict detected: {result.conflict}")
    print("\nConflicting Elements:")
    for element in result.conflicting_elements:
        print(f"\nBank Element: {element.bank_element}")
        print(f"FAS Conflict: {element.fas_conflict}")
        print(f"SS Conflict: {element.ss_conflict}")
    print(f"\nJustification: {result.justification}")
    print(f"\nReferences: {', '.join(result.references)}")

if __name__ == "__main__":
    test_conflict_analysis() 