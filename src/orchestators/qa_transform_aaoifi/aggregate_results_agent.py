"""
Aggregate Results Agent
Purpose: Aggregates outputs from multiple agents into a single, coherent answer.
"""

from typing import Dict, List
from pydantic import BaseModel, Field
from openai import OpenAI
from ...core.config import settings
import json

class AgentOutput(BaseModel):
    """Model for individual agent output."""
    agent: str = Field(description="Name of the agent that produced the output")
    result: str = Field(description="The output/result from the agent")

class AggregationInput(BaseModel):
    """Input model for aggregation analysis."""
    query: str = Field(description="The original user query")
    agent_outputs: List[AgentOutput] = Field(description="List of outputs from different agents")
    aggregation_strategy: str = Field(description="Strategy to use for aggregating results")

class AggregationResult(BaseModel):
    """Model for the aggregated result."""
    final_answer: str = Field(description="The final, aggregated answer to the query")

class AggregateResultsAgent:
    """Agent for aggregating multiple agent outputs into a single answer."""
    
    def __init__(self):
        """Initialize the Aggregate Results agent."""
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.system_prompt = """
You are an expert Shariah-compliant AI analyst.

Given a user query and the structured outputs of several specialized agents, synthesize all results into a single final answer. Justify the answer clearly based on the outputs. Follow the given aggregation strategy.

Guidelines:
1. Maintain Shariah compliance perspective throughout
2. Ensure all relevant findings are incorporated
3. Provide clear justification for the final answer
4. Follow the specified aggregation strategy
5. Keep the answer focused and relevant to the query
6. Use technical accuracy while maintaining clarity
7. Reference specific findings from agent outputs

Respond in JSON format:
{
  "final_answer": "<detailed and justified answer>"
}

The final answer should:
- Directly address the query
- Incorporate all relevant findings
- Provide clear justification
- Maintain technical accuracy
- Be well-structured and coherent
"""

    def aggregate_results(self, input_data: AggregationInput) -> AggregationResult:
        """
        Aggregate multiple agent outputs into a single answer.
        
        Args:
            input_data: AggregationInput object containing query, agent outputs, and strategy
            
        Returns:
            AggregationResult object containing the final answer
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
                return AggregationResult.parse_obj(json_data)
            except json.JSONDecodeError:
                # If not valid JSON, try to parse as string
                return AggregationResult.parse_raw(analysis_data)
            
        except Exception as e:
            print(f"Error aggregating results: {e}")
            raise

    def _format_user_message(self, input_data: AggregationInput) -> str:
        """Format the input data into a structured message for the LLM."""
        return f"""
Query: {input_data.query}

Aggregation Strategy: {input_data.aggregation_strategy}

Agent Outputs:
{json.dumps([output.dict() for output in input_data.agent_outputs], indent=2)}
"""

