"""
Orchestrator for Revising and Updating Regulations Framework
Purpose: Coordinates multiple agents to analyze and update regulations for Shariah compliance.
"""
import sys
import os
from typing import List, Dict, Any

# Add the src directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import json
from pathlib import Path
from src.agents.fas_retriever import FASRetriever, FASDocument
from src.agents.ss_retiever import SSRetriever, SSDocument
from src.agents.summarizer_fas import RetrievalSummarizer
from src.agents.summarizer_ss import SSRetrievalSummarizer
from src.agents.shariah_compliance_agent import ShariahComplianceAgent, ComplianceInput
from src.agents.update_advisor_agent import UpdateAdvisorAgent, UpdateInput

class RegulationRevisionOrchestrator:
    """Orchestrates the process of analyzing and updating regulations for Shariah compliance."""
    
    def __init__(self):
        """Initialize all required agents."""
        self.fas_retriever = FASRetriever()
        self.ss_retriever = SSRetriever()
        self.summarizer_fas = RetrievalSummarizer()
        self.summarizer_ss = SSRetrievalSummarizer()
        self.compliance_agent = ShariahComplianceAgent()
        self.update_advisor = UpdateAdvisorAgent()

    def process_regulations(self, input_json_path: str) -> List[Dict[str, Any]]:
        """
        Process regulations through the complete workflow.
        
        Args:
            input_json_path: Path to the input JSON file containing regulations
            
        Returns:
            List containing the processed and updated regulations
        """
        # Load input JSON
        with open(input_json_path, 'r', encoding='utf-8') as f:
            regulations = json.load(f)
        
        # Process each regulation section
        processed_regulations = []
        for regulation_section in regulations:
            processed_section = {}
            
            # Process External Regulation
            if "External Regulation" in regulation_section:
                processed_section["External Regulation"] = self._process_regulation_list(
                    regulation_section["External Regulation"]
                )
            
            # Process Internal Rulebook
            if "Internal Rulebook" in regulation_section:
                processed_section["Internal Rulebook"] = self._process_regulation_list(
                    regulation_section["Internal Rulebook"]
                )
            
            processed_regulations.append(processed_section)
        
        return processed_regulations

    def _process_regulation_list(self, regulation_list: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        """Process a list of regulations."""
        processed_list = []
        
        for regulation in regulation_list:
            for section_name, content in regulation.items():
                
                
                # Check compliance using proper input model
                compliance_input = ComplianceInput(
                    rule_text=content,
                    ss_summary=""
                )
                compliance_result = self.compliance_agent.check_compliance(compliance_input)
                
                # Create processed regulation entry
                processed_regulation = {
                    section_name: {
                        "original_text": content,
                        "compliance_status": compliance_result.compliance_status,
                        "compliance_justification": compliance_result.justification,
                        "referenced_clauses": compliance_result.referenced_clauses
                    }
                }
                
                # If non-compliant, get update proposal using proper input model
                if compliance_result.compliance_status == "non_compliant":
                    # Extract text content from SS documents for the update proposal
                    ss_documents: List[SSDocument] = self.ss_retriever.retrieve(content)
                    ss_texts = [doc.text for doc in ss_documents]
                    
                    update_input = UpdateInput(
                        non_compliant_text=content,
                        issue_summary=compliance_result.justification,
                        context_type=section_name,
                        ss_documents=ss_texts
                    )
                    update_result = self.update_advisor.propose_update(update_input)
                    
                    processed_regulation[section_name].update({
                        "proposed_update": update_result.proposed_update,
                        "update_rationale": update_result.rationale
                    })
                
                processed_list.append(processed_regulation)
        
        return processed_list

def main():
    """Main function to run the regulation revision process."""
    # Initialize orchestrator
    orchestrator = RegulationRevisionOrchestrator()
    
    # Set up paths
    base_dir = Path(__file__).parent.parent.parent
    input_path = base_dir / "data" / "regulations.json"
    output_path = base_dir / "data" / "updated_regulations.json"
    
    try:
        # Process regulations
        updated_regulations = orchestrator.process_regulations(str(input_path))
        
        # Save output
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(updated_regulations, f, indent=2, ensure_ascii=False)
        
        print(f"Regulations processed successfully. Output saved to {output_path}")
        
    except Exception as e:
        print(f"Error processing regulations: {e}")

if __name__ == "__main__":
    main()
