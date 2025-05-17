"""
Internal Coherence Orchestrator
Purpose: Orchestrates the analysis and revision of cross-border contracts for regulatory coherence.
"""

from typing import List, Dict, Optional
from pydantic import BaseModel, Field
import json
from .internal_coherance.ConflictDetectionAgent import (
    ConflictDetectionAgent,
    ConflictAnalysisInput,
    ContractSection,
    ConflictAnalysisResult,
    ConflictElement
)
from .internal_coherance.ContractRevisor import (
    ContractRevisor,
    RevisionInput,
    RevisionResult
)

class ContractAnnotation(BaseModel):
    """Model for contract section annotations."""
    section_name: str = Field(description="Name of the contract section")
    original_content: str = Field(description="Original content of the section")
    revised_content: Optional[str] = Field(default=None, description="Revised content if auto-revision is possible")
    annotations: List[str] = Field(default_factory=list, description="List of annotations for manual review")
    conflicts: List[Dict] = Field(default_factory=list, description="List of identified conflicts")

class ContractRevision(BaseModel):
    """Model for complete contract revision."""
    contract_path: str = Field(description="Path to the original contract file")
    sections: List[ContractAnnotation] = Field(default_factory=list, description="List of section annotations")
    summary: str = Field(description="Overall summary of revisions and annotations")

class InternalCoherenceOrchestrator:
    """Orchestrator for analyzing and revising cross-border contracts."""
    
    def __init__(self):
        """Initialize the orchestrator."""
        self.conflict_agent = ConflictDetectionAgent()
        self.revisor_agent = ContractRevisor()

    def read_contract_sections(self, contract_path: str) -> List[ContractSection]:
        """Read and parse contract sections from markdown file."""
        sections = []
        current_section = None
        current_content = []
        
        with open(contract_path, 'r') as file:
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

    def analyze_and_revise_contract(self, contract_path: str) -> ContractRevision:
        """
        Analyze and revise a contract for regulatory coherence.
        
        Args:
            contract_path: Path to the contract markdown file
            
        Returns:
            ContractRevision object containing analysis and revisions
        """
        # Read contract sections
        sections = self.read_contract_sections(contract_path)
        section_annotations = []
        
        # Analyze each section
        for section in sections:
            # Get conflict analysis
            input_data = ConflictAnalysisInput(contract_section=section)
            conflict_result = self.conflict_agent.analyze_conflicts(input_data)
            
            # Create annotation
            annotation = ContractAnnotation(
                section_name=section.section_name,
                original_content=section.content,
                conflicts=[conflict.dict() for conflict in conflict_result.conflicts]
            )
            
            # If conflicts exist, generate annotations and potential revisions
            if conflict_result.has_conflicts:
                for conflict in conflict_result.conflicts:
                    # Add annotation for manual review
                    annotation.annotations.append(
                        f"CONFLICT: {conflict.conflict_description}\n"
                        f"IMPACT: {conflict.impact}\n"
                        f"RECOMMENDATION: {conflict.recommendation}"
                    )
                    
                    # Attempt to generate revised content if possible
                    # This is a placeholder - in practice, you might want to use another agent
                    # to generate the actual revisions
                    if not annotation.revised_content:
                        annotation.revised_content = self._generate_revision(
                            section.content,
                            conflict
                        )
            
            section_annotations.append(annotation)
        
        # Generate overall summary
        summary = self._generate_summary(section_annotations)
        
        return ContractRevision(
            contract_path=contract_path,
            sections=section_annotations,
            summary=summary
        )

    def _generate_revision(self, original_content: str, conflict: ConflictElement) -> Optional[str]:
        """
        Generate a revised version of the content based on conflict analysis using ContractRevisor.
        """
        try:
            revision_input = RevisionInput(
                section_name=conflict.section,
                original_content=original_content,
                conflict_description=conflict.conflict_description,
                recommendation=conflict.recommendation
            )
            revision_result = self.revisor_agent.revise_section(revision_input)
            return revision_result.revised_content
        except Exception as e:
            print(f"[Revision Error] {e}")
            return None

    def _generate_summary(self, section_annotations: List[ContractAnnotation]) -> str:
        """Generate an overall summary of the contract analysis."""
        total_conflicts = sum(len(section.conflicts) for section in section_annotations)
        sections_with_conflicts = sum(1 for section in section_annotations if section.conflicts)
        
        summary = f"""
Contract Analysis Summary:
- Total sections analyzed: {len(section_annotations)}
- Sections with conflicts: {sections_with_conflicts}
- Total conflicts identified: {total_conflicts}

Key areas requiring attention:
"""
        
        for section in section_annotations:
            if section.conflicts:
                summary += f"\n{section.section_name}:"
                for conflict in section.conflicts:
                    summary += f"\n- {conflict['conflict_description']}"
        
        return summary

    def save_revision(self, revision: ContractRevision, output_path: str):
        """Save the contract revision to a JSON file."""
        with open(output_path, 'w') as f:
            json.dump(revision.dict(), f, indent=2)
