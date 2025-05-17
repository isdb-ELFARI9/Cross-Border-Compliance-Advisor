import sys
import os

# Add the src directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import json
import asyncio
from src.orchestators.orch_revision_updated_regulation_framework import UpdateRevisionOrchestrator

async def test_orchestrator():
    """Test the Orchestrator's ability to merge reports from ComplianceScannerAgent and PropagatorAgent."""
    print("\nStarting Orchestrator Test")
    print("=========================")
    
    try:
        # Initialize the orchestrator
        print("\nInitializing orchestrator...")
        orchestrator = UpdateRevisionOrchestrator()
        
        # Load input data from data/regulations.json
        print("\nLoading test input data from data/regulations.json...")
        file_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'regulations.json')
        with open(file_path, 'r', encoding='utf-8') as f:
            input_data = json.load(f)
        
        # Orchestrate the agents
        print("\nOrchestrating agents...")
        result = await orchestrator.orchestrate(input_data)
        
        # Print results
        print("\nOrchestration Results:")
        print("=====================")
        print(json.dumps(result, indent=2))
        
        # Save results
        output_path = "./data/orchestration_results.json"
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print(f"\nResults saved to {output_path}")
        
    except Exception as e:
        print(f"\nError during test: {str(e)}")
        print("\nDetailed error information:")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_orchestrator()) 