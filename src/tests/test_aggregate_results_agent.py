"""
Test cases for the Aggregate Results Agent.
"""

import sys
import os
from pathlib import Path

# Add the src directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.orchestators.qa_transform_aaoifi.aggregate_results_agent import (
    AggregateResultsAgent,
    AggregationInput,
    AgentOutput
)

def test_aggregate_results():
    """Test the aggregation functionality."""
    # Initialize the agent
    aggregator = AggregateResultsAgent()
    
    # Create test input
    input_data = AggregationInput(
        query="What are the compliance risks with current liquidity policies?",
        agent_outputs=[
            AgentOutput(
                agent="RiskDetectionAgent",
                result="Identified potential non-compliance in risk quantification methods. Current approach may not fully align with AAOIFI standards for liquidity risk assessment."
            ),
            AgentOutput(
                agent="ConflictDetectionAgent",
                result="Found conflict with AAOIFI principle of profit-sharing under stress scenarios. Current policy allows for fixed returns during liquidity stress periods."
            )
        ],
        aggregation_strategy="Summarize findings from both agents to answer the query with justification."
    )
    
    # Get the aggregated result
    result = aggregator.aggregate_results(input_data)
    
    # Print the results
    print("\nTest Query:", input_data.query)
    print("\nAggregation Strategy:", input_data.aggregation_strategy)
    print("\nAgent Outputs:")
    for output in input_data.agent_outputs:
        print(f"\n{output.agent}:")
        print(output.result)
    print("\nFinal Aggregated Answer:")
    print(result.final_answer)
    
    # Basic assertions
    assert result.final_answer
    assert len(result.final_answer) > 0
    # Check if the answer incorporates key elements from both agent outputs
    assert "risk" in result.final_answer.lower()
    assert "compliance" in result.final_answer.lower()
    assert "AAOIFI" in result.final_answer

if __name__ == "__main__":
    test_aggregate_results() 