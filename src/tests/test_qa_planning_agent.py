"""
Test cases for the QA Planning Agent.
"""

import sys
import os
from pathlib import Path

# Add the src directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.orchestators.qa_transform_aaoifi.QA_planning_agent import (
    QAPlanningAgent,
    PlanningInput
)

def test_create_plan():
    """Test the planning functionality."""
    # Initialize the agent
    planner = QAPlanningAgent()
    
    # Create test input
    input_data = PlanningInput(
        query="What are the compliance risks with current liquidity policies?",
        relevant_parts={
            "External Regulation": ["Liquidity Rules & Funding"],
            "Internal Rulebook": ["Risk Management Framework"]
        }
    )
    
    # Get the execution plan
    result = planner.create_plan(input_data)
    
    # Print the results
    print("\nTest Query:", input_data.query)
    print("\nRelevant Parts:", input_data.relevant_parts)
    print("\nExecution Plan:")
    for i, step in enumerate(result.steps, 1):
        print(f"\nStep {i}:")
        print(f"Agent: {step.agent}")
        print(f"Input Sections: {step.input_sections}")
        print(f"Reason: {step.reason}")
    print(f"\nFinal Aggregation Strategy: {result.final_aggregation_strategy}")
    
    # Basic assertions
    assert len(result.steps) > 0
    assert result.final_aggregation_strategy
    for step in result.steps:
        assert step.agent in ["AmbiguityDetectionAgent", "GapDetectionAgent", 
                            "ConflictDetectionAgent", "RiskDetectionAgent"]
        assert len(step.input_sections) > 0
        assert step.reason

if __name__ == "__main__":
    test_create_plan() 