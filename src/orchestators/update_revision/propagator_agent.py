"""
Propagator Agent
Purpose: Distributes compliance scanner results to specialized agents for parallel analysis.
"""

from typing import Dict, List, Any
from pydantic import BaseModel, Field
from openai import OpenAI
from ...core.config import settings
from .compliance_scanner_agent import ProblematicField
from ...agents.ambiguity_agent import AmbiguityDetectionAgent, AmbiguityAnalysisInput
from ...agents.gap_agent import GapDetectionAgent, GapAnalysisInput
from ...agents.conflict_agent import ConflictDetectionAgent, ConflictAnalysisInput
from ...agents.risk_agent import RiskAnalysisAgent, RiskAnalysisInput
import json
import asyncio
from concurrent.futures import ThreadPoolExecutor

class AgentReport(BaseModel):
    """Model for individual agent analysis report."""
    agent_name: str = Field(description="Name of the specialized agent")
    field_location: str = Field(description="Location of the analyzed field")
    analysis_result: Dict[str, Any] = Field(description="Analysis result from the agent")
    severity: str = Field(
        description="Severity level: high, medium, or low",
        pattern="^(high|medium|low)$"
    )

class PropagationResult(BaseModel):
    """Model for the complete propagation result."""
    field_reports: Dict[str, List[AgentReport]] = Field(
        description="Reports from all agents for each problematic field"
    )

class PropagatorAgent:
    """Agent for distributing compliance scanner results to specialized agents."""
    
    def __init__(self):
        """Initialize the Propagator agent and specialized agents."""
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.executor = ThreadPoolExecutor(max_workers=4)
        
        # Initialize specialized agents
        self.ambiguity_agent = AmbiguityDetectionAgent()
        self.gap_agent = GapDetectionAgent()
        self.conflict_agent = ConflictDetectionAgent()
        self.risk_agent = RiskAnalysisAgent()

    async def propagate(self, problematic_fields: List[ProblematicField]) -> PropagationResult:
        """
        Distribute problematic fields to specialized agents for parallel analysis.
        
        Args:
            problematic_fields: List of problematic fields from compliance scanner
            
        Returns:
            PropagationResult containing reports from all agents
        """
        try:
            field_reports = {}
            
            # Process each problematic field
            for field in problematic_fields:
                # Create tasks for parallel processing
                tasks = [
                    self._analyze_ambiguity(field),
                    self._analyze_gaps(field),
                    self._analyze_conflicts(field),
                    self._analyze_risks(field)
                ]
                
                # Wait for all agents to complete their analysis
                reports = await asyncio.gather(*tasks)
                field_reports[field.location] = reports
            
            return PropagationResult(field_reports=field_reports)
            
        except Exception as e:
            print(f"Error propagating to agents: {e}")
            raise

    async def _analyze_ambiguity(self, field: ProblematicField) -> AgentReport:
        """Analyze field using AmbiguityDetectionAgent."""
        try:
            input_data = AmbiguityAnalysisInput(
                rule_text=field.text,
                fas_summary="",  # TODO: Get relevant FAS summary
                ss_summary=field.justification
            )
            
            result = await asyncio.get_event_loop().run_in_executor(
                self.executor,
                lambda: self.ambiguity_agent.analyze_ambiguity(input_data)
            )
            
            return AgentReport(
                agent_name="Ambiguity Detection Agent",
                field_location=field.location,
                analysis_result=result.dict(),
                severity="high" if result.ambiguous else "low"
            )
        except Exception as e:
            print(f"Error in ambiguity analysis: {e}")
            raise

    async def _analyze_gaps(self, field: ProblematicField) -> AgentReport:
        """Analyze field using GapDetectionAgent."""
        try:
            input_data = GapAnalysisInput(
                rule_text=field.text,
                fas_summary="",  # TODO: Get relevant FAS summary
                ss_summary=field.justification
            )
            
            result = await asyncio.get_event_loop().run_in_executor(
                self.executor,
                lambda: self.gap_agent.analyze_gaps(input_data)
            )
            
            return AgentReport(
                agent_name="Gap Detection Agent",
                field_location=field.location,
                analysis_result=result.dict(),
                severity="high" if result.has_gaps else "low"
            )
        except Exception as e:
            print(f"Error in gap analysis: {e}")
            raise

    async def _analyze_conflicts(self, field: ProblematicField) -> AgentReport:
        """Analyze field using ConflictDetectionAgent."""
        try:
            input_data = ConflictAnalysisInput(
                rule_text=field.text,
                fas_summary="",  # TODO: Get relevant FAS summary
                ss_summary=field.justification
            )
            
            result = await asyncio.get_event_loop().run_in_executor(
                self.executor,
                lambda: self.conflict_agent.analyze_conflict(input_data)
            )
            
            return AgentReport(
                agent_name="Conflict Detection Agent",
                field_location=field.location,
                analysis_result=result.dict(),
                severity="high" if result.conflict else "low"
            )
        except Exception as e:
            print(f"Error in conflict analysis: {e}")
            raise

    async def _analyze_risks(self, field: ProblematicField) -> AgentReport:
        """Analyze field using RiskAnalysisAgent."""
        try:
            input_data = RiskAnalysisInput(
                product_description=field.text,
                standard="",  # TODO: Get relevant standard
                known_risks=field.referenced_clauses
            )
            
            result = await asyncio.get_event_loop().run_in_executor(
                self.executor,
                lambda: self.risk_agent.analyze_risk(input_data)
            )
            
            # Ensure analysis_result is a valid dictionary
            analysis_result = result.dict() if hasattr(result, 'dict') else {}
            
            # Determine severity based on risk analysis
            severity = "high" if any(r.severity.lower() == "high" for r in result.risks) else \
                      "medium" if any(r.severity.lower() == "medium" for r in result.risks) else "low"
            
            return AgentReport(
                agent_name="Risk Analysis Agent",
                field_location=field.location,
                analysis_result=analysis_result,
                severity=severity
            )
        except Exception as e:
            print(f"Error in risk analysis: {e}")
            raise 