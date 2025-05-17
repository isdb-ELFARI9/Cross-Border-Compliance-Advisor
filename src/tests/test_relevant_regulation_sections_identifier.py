"""
Test cases for the Relevant Regulation Sections Identifier agent.
"""

import sys
import os
from pathlib import Path

# Add the src directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.agents.relevant_regulation_sections_identifier import (
    RelevantRegulationSectionsIdentifier,
    QueryInput
)

def test_identify_sections():
    """Test the section identification functionality."""
    # Initialize the agent
    identifier = RelevantRegulationSectionsIdentifier()
    
    # Create a test query
    query = "How is liquidity risk handled?"
    input_data = QueryInput(query=query)
    
    # Get the relevant sections
    result = identifier.identify_sections(input_data)
    
    # Print the results
    print("\nTest Query:", query)
    print("\nIdentified Sections:")
    print("External Regulation:", result.external_regulation)
    print("Internal Rulebook:", result.internal_rulebook)
    
    # Basic assertions
    assert isinstance(result.external_regulation, list)
    assert isinstance(result.internal_rulebook, list)
    assert "Liquidity Rules & Funding" in result.external_regulation
    assert "Risk Management Framework" in result.internal_rulebook

if __name__ == "__main__":
    test_identify_sections() 