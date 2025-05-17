"""
Simple test script for InternalCoherenceOrchestrator
"""

import sys
import os

# Add the src directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from src.cross_border_compliance.InternalCoherenceOrchestrator import (
    InternalCoherenceOrchestrator,
    ContractRevision,
    ContractAnnotation
)

def test_orchestrator():
    """Simple test function for InternalCoherenceOrchestrator"""
    print("\n=== Testing InternalCoherenceOrchestrator ===\n")
    
    # Initialize orchestrator
    print("1. Initializing orchestrator...")
    orchestrator = InternalCoherenceOrchestrator()
    print("✓ Orchestrator initialized successfully\n")
    
    # Test contract path
    contract_path = 'D:/Isdbi/CompliabceAdvisor/data_cross_border/draft_contract.md'
    
    # Test reading contract sections
    print("2. Reading contract sections...")
    sections = orchestrator.read_contract_sections(contract_path)
    print(f"✓ Successfully read {len(sections)} sections:")
    for section in sections:
        print(f"  - {section.section_name}")
    print()
    
    # Test analyzing and revising contract
    print("3. Analyzing contract for conflicts...")
    revision = orchestrator.analyze_and_revise_contract(contract_path)
    print("✓ Contract analysis completed")
    print(f"\nAnalysis Summary:\n{revision.summary}\n")
    
    # Print detailed results for each section
    print("4. Detailed Analysis Results:")
    print("=" * 80)
    for section in revision.sections:
        print(f"\nSection: {section.section_name}")
        print("-" * 40)
        print(f"Original Content:\n{section.original_content}")
        
        if section.conflicts:
            print("\nIdentified Conflicts:")
            for conflict in section.conflicts:
                print(f"\n- Description: {conflict['conflict_description']}")
                print(f"  Impact: {conflict['impact']}")
                print(f"  Recommendation: {conflict['recommendation']}")
        
        if section.annotations:
            print("\nAnnotations:")
            for annotation in section.annotations:
                print(f"\n{annotation}")
        
        if section.revised_content:
            print("\nProposed Revision:")
            print(section.revised_content)
        
        print("\n" + "=" * 80)
    
    # Test saving revision
    print("\n5. Saving revision to file...")
    output_path = 'D:/Isdbi/CompliabceAdvisor/data_cross_border/contract_revision.json'
    orchestrator.save_revision(revision, output_path)
    print(f"✓ Revision saved to: {output_path}")
    
    print("\n=== Test Completed Successfully ===\n")

if __name__ == "__main__":
    test_orchestrator() 