"""
Simple test script for ConflictDetectionAgent using draft contract
"""
import sys
import os
from typing import List

# Add the src directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.cross_border_compliance.internal_coherance.ConflictDetectionAgent import (
    ConflictDetectionAgent,
    ConflictAnalysisInput,
    ContractSection
)

def read_contract_sections():
    """Read and parse contract sections from draft_contract.md"""
    sections = []
    current_section = None
    current_content = []
    
    with open('D:/Isdbi/CompliabceAdvisor/data_cross_border/draft_contract.md', 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('###'):
                # Save previous section if exists
                if current_section and current_content:
                    sections.append(ContractSection(
                        section_name=current_section,
                        content='\n'.join(current_content)
                    ))
                # Start new section
                current_section = line.replace('###', '').strip()
                current_content = []
            elif line and not line.startswith('---'):
                current_content.append(line)
    
    # Add last section
    if current_section and current_content:
        sections.append(ContractSection(
            section_name=current_section,
            content='\n'.join(current_content)
        ))
    
    return sections

def main():
    # Initialize the agent
    agent = ConflictDetectionAgent()

    # Read contract sections
    contract_sections = read_contract_sections()

    # Analyze each section
    print("\nAnalyzing contract sections for conflicts...\n")
    
    for section in contract_sections:
        print(f"\n{'='*80}")
        print(f"Analyzing section: {section.section_name}")
        print(f"{'='*80}")
        print(f"\nContent:\n{section.content}")
        
        # Create input for analysis
        input_data = ConflictAnalysisInput(
            contract_section=section
        )
        
        # Get analysis results
        result = agent.analyze_conflicts(input_data)
        
        # Print results
        print(f"\nHas Conflicts: {result.has_conflicts}")
        print(f"\nSummary: {result.summary}")
        
        if result.conflicts:
            print("\nIdentified Conflicts:")
            for conflict in result.conflicts:
                print(f"\nSection: {conflict.section}")
                print(f"Description: {conflict.conflict_description}")
                print(f"Impact: {conflict.impact}")
                print(f"Recommendation: {conflict.recommendation}")
        
        print("\n" + "-"*80)

if __name__ == "__main__":
    main() 