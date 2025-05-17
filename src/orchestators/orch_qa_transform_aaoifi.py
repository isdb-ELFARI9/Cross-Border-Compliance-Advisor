"""
QA Transform AAOIFI Orchestrator
Purpose: Orchestrates the process of answering regulatory queries using multiple specialized agents.
"""

import sys
import os
from typing import Dict, List, Any
from pathlib import Path
import json

# Add the src directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.orchestators.qa_transform_aaoifi.relevant_regulation_sections_identifier import (
    RelevantRegulationSectionsIdentifier,
    QueryInput as SectionsQueryInput
)
from src.orchestators.qa_transform_aaoifi.QA_planning_agent import (
    QAPlanningAgent,
    PlanningInput as PlanningQueryInput
)
from src.orchestators.qa_transform_aaoifi.aggregate_results_agent import (
    AggregateResultsAgent,
    AggregationInput,
    AgentOutput
)

class QATransformOrchestrator:
    """Orchestrates the process of answering regulatory queries using multiple agents."""
    
    def __init__(self):
        """Initialize all required agents."""
        self.sections_identifier = RelevantRegulationSectionsIdentifier()
        self.planning_agent = QAPlanningAgent()
        self.aggregate_agent = AggregateResultsAgent()
        
        # Initialize specialized agents
        self.ambiguity_agent = None  # To be implemented
        self.gap_agent = None  # To be implemented
        self.conflict_agent = None  # To be implemented
        self.risk_agent = None  # To be implemented

    def process_query(self, query: str) -> Dict[str, Any]:
        """
        Process a regulatory query through the complete workflow.
        
        Args:
            query: The user's query to process
            
        Returns:
            Dictionary containing the complete analysis process and final answer
        """
        try:
            # Step 1: Identify relevant regulation sections
            sections_input = SectionsQueryInput(query=query)
            sections_result = self.sections_identifier.identify_sections(sections_input)
            
            # Step 2: Create execution plan
            planning_input = PlanningQueryInput(
                query=query,
                relevant_parts={
                    "External Regulation": sections_result.external_regulation,
                    "Internal Rulebook": sections_result.internal_rulebook
                }
            )
            planning_result = self.planning_agent.create_plan(planning_input)
            
            # Step 3: Execute each step in the plan (placeholder for now)
            agent_outputs = []
            for step in planning_result.steps:
                # TODO: Implement actual agent execution
                # For now, create placeholder outputs
                agent_output = AgentOutput(
                    agent=step.agent,
                    result=f"Placeholder result from {step.agent} for sections: {', '.join(step.input_sections)}"
                )
                agent_outputs.append(agent_output)
            
            # Step 4: Aggregate results
            aggregation_input = AggregationInput(
                query=query,
                agent_outputs=agent_outputs,
                aggregation_strategy=planning_result.final_aggregation_strategy
            )
            final_result = self.aggregate_agent.aggregate_results(aggregation_input)
            
            # Create complete output
            output = {
                "query": query,
                "analysis_process": {
                    "relevant_sections": {
                        "external_regulation": sections_result.external_regulation,
                        "internal_rulebook": sections_result.internal_rulebook
                    },
                    "execution_plan": {
                        "steps": [
                            {
                                "agent": step.agent,
                                "input_sections": step.input_sections,
                                "reason": step.reason
                            }
                            for step in planning_result.steps
                        ],
                        "aggregation_strategy": planning_result.final_aggregation_strategy
                    },
                    "agent_outputs": [
                        {
                            "agent": output.agent,
                            "result": output.result
                        }
                        for output in agent_outputs
                    ]
                },
                "final_answer": final_result.final_answer
            }
            
            return output
            
        except Exception as e:
            print(f"Error processing query: {e}")
            raise

def main():
    """Main function to run the QA transformation process."""
    # Initialize orchestrator
    orchestrator = QATransformOrchestrator()
    
    # Example query
    query = "What are the compliance risks with current liquidity policies?"
    
    try:
        # Process query
        result = orchestrator.process_query(query)
        
        # Save output
        output_path = Path(__file__).parent.parent.parent / "data" / "qa_analysis_result.json"
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print(f"Query processed successfully. Output saved to {output_path}")
        
    except Exception as e:
        print(f"Error processing query: {e}")

if __name__ == "__main__":
    main()
