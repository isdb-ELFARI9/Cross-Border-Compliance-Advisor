import sys
import os

# Add the src directory to Python path

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import json
import asyncio
from src.orchestators.update_revision.propagator_agent import PropagatorAgent
from src.orchestators.update_revision.compliance_scanner_agent import ComplianceScannerAgent, ProblematicField

async def test_propagator_agent():
    """Test the PropagatorAgent's ability to distribute and analyze problematic fields."""
    print("\nStarting PropagatorAgent Test")
    print("=============================")
    
    try:
        # Initialize agents
        print("\nInitializing agents...")
        scanner = ComplianceScannerAgent()
        propagator = PropagatorAgent()
        
        # Example problematic field
        print("\nCreating test problematic field...")
        problematic_field = ProblematicField(
            location="External Regulation > Liquidity Rules & Funding",
            text="Banks must maintain adequate liquidity ratios.",
            compliance_status="partially_compliant",
            justification="Missing specific liquidity ratio requirements",
            referenced_clauses=["SS-1.1", "SS-3.2"]
        )
        
        # Propagate to specialized agents
        print("\nPropagating to specialized agents...")
        result = await propagator.propagate([problematic_field])
        
        # Print results
        print("\nPropagation Results:")
        print("===================")
        for location, reports in result.field_reports.items():
            print(f"\nLocation: {location}")
            for report in reports:
                print(f"\nAgent: {report.agent_name}")
                print(f"Analysis Result: {json.dumps(report.analysis_result, indent=2)}")
                print(f"Severity: {report.severity}")
                print("-" * 50)
        
        # Save results
        output_path = "D:/Isdbi/CompliabceAdvisor/data/propagation_results.json"
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result.dict(), f, indent=2, ensure_ascii=False)
        
        print(f"\nResults saved to {output_path}")
        
    except Exception as e:
        print(f"\nError during test: {str(e)}")
        print("\nDetailed error information:")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_propagator_agent()) 