"""
Orchestrator for Revising and Updating Regulations Framework
Purpose: Coordinates multiple agents to analyze and update regulations for Shariah compliance.
"""

from typing import Dict, List, Any
import json
from pathlib import Path
from ..agents.fas_retriever import FASRetriever
from ..agents.ss_retriever import SSRetriever
from ..agents.summarizer_fas import SummarizerFAS
from ..agents.summarizer_ss import SummarizerSS
from ..agents.shariah_compliance_agent import ShariahComplianceAgent, ComplianceInput
from ..agents.update_advisor_agent import UpdateAdvisorAgent, UpdateInput

class RegulationRevisionOrchestrator:
    """Orchestrates the process of analyzing and updating regulations for Shariah compliance."""
    
    def __init__(self):
        """Initialize all required agents."""
        self.fas_retriever = FASRetriever()
        self.ss_retriever = SSRetriever()
        self.summarizer_fas = SummarizerFAS()
        self.summarizer_ss = SummarizerSS()
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
                # Get relevant FAS and SS texts
                fas_text = self.fas_retriever.retrieve_fas(content)
                ss_text = self.ss_retriever.retrieve_ss(content)
                
                # Summarize the texts
                fas_summary = self.summarizer_fas.summarize(fas_text)
                ss_summary = self.summarizer_ss.summarize(ss_text)
                
                # Check compliance
                compliance_result = self._check_compliance(content, ss_summary)
                
                # Create processed regulation entry
                processed_regulation = {
                    section_name: {
                        "original_text": content,
                        "compliance_status": compliance_result.compliance_status,
                        "compliance_justification": compliance_result.justification,
                        "referenced_clauses": compliance_result.referenced_clauses
                    }
                }
                
                # If non-compliant, get update proposal
                if compliance_result.compliance_status == "non_compliant":
                    update_result = self._get_update_proposal(
                        content,
                        compliance_result.justification,
                        section_name,
                        ss_text
                    )
                    processed_regulation[section_name].update({
                        "proposed_update": update_result.proposed_update,
                        "update_rationale": update_result.rationale
                    })
                
                processed_list.append(processed_regulation)
        
        return processed_list

    def _check_compliance(self, rule_text: str, ss_summary: str) -> Any:
        """Check compliance of a rule using the ShariahComplianceAgent."""
        input_data = ComplianceInput(
            rule_text=rule_text,
            ss_summary=ss_summary
        )
        return self.compliance_agent.check_compliance(input_data)

    def _get_update_proposal(
        self,
        non_compliant_text: str,
        issue_summary: str,
        context_type: str,
        ss_documents: List[str]
    ) -> Any:
        """Get update proposal using the UpdateAdvisorAgent."""
        input_data = UpdateInput(
            non_compliant_text=non_compliant_text,
            issue_summary=issue_summary,
            context_type=context_type,
            ss_documents=ss_documents
        )
        return self.update_advisor.propose_update(input_data)

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
