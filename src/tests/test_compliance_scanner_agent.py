"""
Test cases for the Compliance Scanner Agent.
"""

import sys
import os
from pathlib import Path
import json

# Add the src directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.orchestators.update_revision.compliance_scanner_agent import ComplianceScannerAgent
from data.regulation_data import RegulationData

def test_scan_draft():
    """Test scanning a regulation draft for compliance issues."""
    # Initialize the agent
    scanner = ComplianceScannerAgent()
    
    # Load test data
    regulation_data = RegulationData("D:/Isdbi/CompliabceAdvisor/data/regulations.json")
    
    # Create draft regulation structure
    draft_regulation = {
        "External Regulation": [
            {key: regulation_data.get("external", key)}
            for key in regulation_data.list_sections("external")
        ],
        "Internal Rulebook": [
            {key: regulation_data.get("internal", key)}
            for key in regulation_data.list_sections("internal")
        ]
    }
    
    # Scan the draft
    result = scanner.scan_draft(draft_regulation)
    
    # Print results for inspection
    print("\nCompliance Scan Results:")
    print("=======================")
    for field in result.problematic_fields:
        print(f"\nLocation: {field.location}")
        print(f"Status: {field.compliance_status}")
        print(f"Justification: {field.justification}")
        print(f"Referenced Clauses: {', '.join(field.referenced_clauses)}")
        print("-" * 50)
    
    # Basic assertions
    assert isinstance(result.problematic_fields, list)
    
    # Save results to file for inspection
    output_path = Path("D:/Isdbi/CompliabceAdvisor/data") / "compliance_scan_results.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result.dict(), f, indent=2, ensure_ascii=False)
    
    print(f"\nResults saved to {output_path}")

if __name__ == "__main__":
    test_scan_draft() 