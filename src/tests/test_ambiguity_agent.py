"""
Test script for the AmbiguityDetectionAgent.
"""

import sys
import os

# Add the src directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.agents.ambiguity_agent import (
    AmbiguityDetectionAgent,
    AmbiguityAnalysisInput
)

def main():
    """Test ambiguity analysis with a simple Murabaha contract rule."""
    # Create agent instance
    agent = AmbiguityDetectionAgent()
    
    # Create test input
    input_data = AmbiguityAnalysisInput(
        rule_text="""
        The bank will determine the profit margin based on market conditions and customer relationship.
        The profit will be distributed fairly between the bank and the customer.
        The contract terms may be modified at the bank's discretion.
        """,
        fas_summary="""
        FAS 28 (Murabaha) requires clear specification of profit margins and distribution terms.
        All contract terms must be fixed and certain at the time of contract.
        """,
        ss_summary="""
        Shariah Standard No. 1 (Murabaha) requires certainty in contract terms and pricing.
        Profit distribution must be clearly specified and agreed upon at contract initiation.
        """
    )
    
    try:
        # Get analysis result
        result = agent.analyze_ambiguity(input_data)
        
        # Print the analysis result
        print("\n=== Ambiguity Analysis Results ===")
        print(f"\nAmbiguous: {result.ambiguous}")
        
        if result.ambiguous:
            print("\nAmbiguous Elements:")
            for element in result.ambiguous_elements:
                print(f"\nText: {element.text}")
                print(f"Reason: {element.reason}")
                print(f"Required Clarification: {element.required_clarification}")
        else:
            print("\nNo ambiguities found in the rule.")
            
    except Exception as e:
        print(f"Error during analysis: {e}")

if __name__ == "__main__":
    main() 