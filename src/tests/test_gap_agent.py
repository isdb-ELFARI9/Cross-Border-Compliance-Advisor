"""
Test script for the GapDetectionAgent.
"""

import sys
import os

# Add the src directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.agents.gap_agent import (
    GapDetectionAgent,
    GapAnalysisInput
)

def main():
    """Test gap analysis with a simple Murabaha contract rule."""
    # Create agent instance
    agent = GapDetectionAgent()
    
    # Create test input
    input_data = GapAnalysisInput(
        rule_text="""
        The bank will purchase goods from the supplier and sell them to the customer at a markup.
        The customer will pay in monthly installments over 12 months.
        Late payment fees will be charged at 2% per month.
        """,
        fas_summary="""
        FAS 28 (Murabaha) requires:
        - Clear specification of cost price and markup
        - Detailed payment terms and conditions
        - Risk transfer conditions
        - Asset ownership transfer details
        - Prohibition of late payment fees that increase debt
        """,
        ss_summary="""
        Shariah Standard No. 1 (Murabaha) requires:
        - Complete asset specifications
        - Clear pricing mechanism
        - Proper risk transfer documentation
        - No penalty fees that increase debt
        - Proper disclosure of all terms
        """
    )
    
    try:
        # Get analysis result
        result = agent.analyze_gaps(input_data)
        
        # Print the analysis result
        print("\n=== Gap Analysis Results ===")
        print(f"\nHas Gaps: {result.has_gaps}")
        
        if result.has_gaps:
            print("\nMissing Elements:")
            for element in result.missing_elements:
                print(f"\nRequirement: {element.requirement}")
                print(f"Importance: {element.importance}")
                print(f"Recommendation: {element.recommendation}")
        else:
            print("\nNo gaps found in the rule.")
            
    except Exception as e:
        print(f"Error during analysis: {e}")

if __name__ == "__main__":
    main() 