"""
API Client for Cross-Border Compliance Advisor
Purpose: Provides a Python client for interacting with the API.
"""

import requests
import json
from typing import Dict, Any, List, Optional

class ComplianceAdvisorClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        """
        Initialize the client with the API base URL.
        
        Args:
            base_url: The base URL of the API server
        """
        self.base_url = base_url.rstrip('/')
    
    def health_check(self) -> Dict[str, Any]:
        """Check if the API is healthy and all services are available."""
        response = requests.get(f"{self.base_url}/health")
        response.raise_for_status()
        return response.json()
    
    def process_qa_query(self, query: str) -> Dict[str, Any]:
        """
        Process a regulatory query and get a comprehensive answer.
        
        Args:
            query: The regulatory query to process
            
        Returns:
            Dictionary containing the analysis process and final answer
        """
        payload = {"text": query}
        response = requests.post(f"{self.base_url}/api/qa-transform", json=payload)
        response.raise_for_status()
        return response.json()
    
    def process_regulation_drafting(self, regulations: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process regulations for Shariah compliance analysis.
        
        Args:
            regulations: Dictionary containing regulations to process
            
        Returns:
            Dictionary containing processed regulations with compliance status
        """
        payload = {"regulations": regulations}
        response = requests.post(f"{self.base_url}/api/regulation-drafting", json=payload)
        response.raise_for_status()
        return response.json()
    
    def process_regulation_update(self, regulations: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze regulations for compliance issues.
        
        Args:
            regulations: Dictionary containing regulations to analyze
            
        Returns:
            Dictionary containing the final review report
        """
        payload = {"regulations": regulations}
        response = requests.post(f"{self.base_url}/api/regulation-update", json=payload)
        response.raise_for_status()
        return response.json()

if __name__ == "__main__":
    # Example usage
    client = ComplianceAdvisorClient()
    
    # Check health
    print("Checking API health...")
    health = client.health_check()
    print(f"Health status: {health}")
    
    # Process a query
    print("\nProcessing query...")
    query_result = client.process_qa_query("What are the compliance risks with current liquidity policies?")
    print(f"Final answer: {query_result.get('final_answer', 'No answer available')}")
    
    # Load and process regulations
    try:
        import os
        from pathlib import Path
        
        regulations_path = Path(os.path.dirname(os.path.abspath(__file__))) / "data" / "regulations.json"
        with open(regulations_path, 'r', encoding='utf-8') as f:
            regulations = json.load(f)
        
        print("\nProcessing regulations drafting...")
        drafting_result = client.process_regulation_drafting(regulations)
        print(f"Processed {len(drafting_result.get('processed_regulations', []))} regulation sections")
        
        print("\nProcessing regulations update...")
        update_result = client.process_regulation_update(regulations)
        print(f"Issues found: {sum(len(issues) for issues in update_result.get('final_review_report', {}).values())}")
        
    except Exception as e:
        print(f"Error in example: {e}")
