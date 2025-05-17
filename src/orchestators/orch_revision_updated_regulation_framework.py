"""
Orchestration Module for Compliance Scanner and Propagator Agents
Purpose: Merges reports from ComplianceScannerAgent and PropagatorAgent into a single structured document.
"""

import json
from typing import Dict, List, Any
from .update_revision.compliance_scanner_agent import ComplianceScannerAgent, ProblematicField
from .update_revision.propagator_agent import PropagatorAgent, PropagationResult

class UpdateRevisionOrchestrator:
    def __init__(self):
        self.scanner = ComplianceScannerAgent()
        self.propagator = PropagatorAgent()

    async def orchestrate(self, input_data: Dict[str, Any]) -> Dict[str, List[Any]]:
        """
        Orchestrate the compliance scanner and propagator agents to merge their reports.

        Args:
            input_data: Input data for the compliance scanner.

        Returns:
            A structured document containing merged reports.
        """
        # Step 1: Run the compliance scanner
        problematic_fields = self.scanner.scan_draft(input_data)

        # Step 2: Propagate the problematic fields to specialized agents
        propagation_result = await self.propagator.propagate(problematic_fields.problematic_fields)

        # Step 3: Merge the reports into a single structured document
        final_review_report = {
            "Ambiguity": [],
            "Gap": [],
            "Conflict": [],
            "Risk": []
        }

        for location, reports in propagation_result.field_reports.items():
            for report in reports:
                if report.agent_name == "Ambiguity Detection Agent":
                    final_review_report["Ambiguity"].append(report.analysis_result)
                elif report.agent_name == "Gap Detection Agent":
                    final_review_report["Gap"].append(report.analysis_result)
                elif report.agent_name == "Conflict Detection Agent":
                    final_review_report["Conflict"].append(report.analysis_result)
                elif report.agent_name == "Risk Analysis Agent":
                    final_review_report["Risk"].append(report.analysis_result)

        return {"final_review_report": final_review_report}

