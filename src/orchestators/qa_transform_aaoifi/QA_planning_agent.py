"""
QA Planning Agent
Purpose: Creates a reasoning-based execution plan for answering regulatory queries using specialized agents.
"""

from typing import Dict, List
from pydantic import BaseModel, Field
from openai import OpenAI
from src.core.config import settings  
import json

class PlanningStep(BaseModel):
    """Model for a single planning step."""
    agent: str = Field(description="The agent to use for this step")
    input_sections: List[str] = Field(description="The sections to apply the agent to")
    reason: str = Field(description="The reason for selecting this agent")

class PlanningResult(BaseModel):
    """Model for the complete planning result."""
    steps: List[PlanningStep] = Field(description="List of planning steps")
    final_aggregation_strategy: str = Field(description="Strategy to aggregate results into final answer")

class PlanningInput(BaseModel):
    """Input model for planning analysis."""
    query: str = Field(description="The user's query to analyze")
    relevant_parts: Dict[str, List[str]] = Field(description="Relevant regulation sections")

class QAPlanningAgent:
    """Agent for creating execution plans to answer regulatory queries."""
    
    def __init__(self):
        """Initialize the QA Planning agent."""
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.system_prompt = """
You are a Shariah-compliant regulatory planner.

Given a user query and the relevant sections of a regulation document, generate a step-by-step execution plan. The goal is to determine which specialized agents (from: AmbiguityDetectionAgent, GapDetectionAgent, ConflictDetectionAgent, RiskDetectionAgent) should be used and on which parts.

Each step should specify:
- The agent to use
- The sections to apply it to
- The reason for selecting that agent

Then, specify how to aggregate the results into a final answer.

Available Agents:
1. AmbiguityDetectionAgent: Detects unclear or ambiguous language in regulations
2. GapDetectionAgent: Identifies missing elements required by AAOIFI standards
3. ConflictDetectionAgent: Finds contradictions with AAOIFI standards
4. RiskDetectionAgent: Evaluates compliance risk exposure

Guidelines:
1. Choose agents based on query intent and section content
2. Order steps logically (e.g., check conflicts before gaps)
3. Be specific about which sections each agent should analyze
4. Provide clear reasoning for each agent selection
5. Specify how to combine results into a coherent answer

Respond in JSON format:
{
  "steps": [
    {
      "agent": "AgentName",
      "input_sections": ["section1", "section2"],
      "reason": "explanation"
    }
  ],
  "final_aggregation_strategy": "strategy description"
}
"""

    def create_plan(self, input_data: PlanningInput) -> PlanningResult:
        """
        Create an execution plan for answering a regulatory query.
        
        Args:
            input_data: PlanningInput object containing query and relevant sections
            
        Returns:
            PlanningResult object containing the execution plan
        """
        try:
            # Format the user message
            user_message = self._format_user_message(input_data)
            
            # Get analysis from OpenAI
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.2,
                response_format={"type": "json_object"}
            )
            
            # Parse the response
            analysis_data = response.choices[0].message.content
            # Try to parse as JSON first
            try:
                json_data = json.loads(analysis_data)
                return PlanningResult.parse_obj(json_data)
            except json.JSONDecodeError:
                # If not valid JSON, try to parse as string
                return PlanningResult.parse_raw(analysis_data)
            
        except Exception as e:
            print(f"Error creating execution plan: {e}")
            raise

    def _format_user_message(self, input_data: PlanningInput) -> str:
        """Format the input data into a structured message for the LLM."""
        return f"""
Query: {input_data.query}

Relevant Parts:
{json.dumps(input_data.relevant_parts, indent=2)}
""" 