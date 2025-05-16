"""
Test script for the Retrieval Summarizer agent.
"""

import sys
from pathlib import Path
import unittest
from typing import Dict, List

# Add the project root directory to Python path
project_root = str(Path(__file__).parent.parent.parent)
sys.path.append(project_root)

from src.agents.fas_retriever import FASRetriever, FASDocument
from src.agents.summarizer_fas import RetrievalSummarizer

class TestRetrievalSummarizer(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.retriever = FASRetriever()
        self.summarizer = RetrievalSummarizer()
    def test_document_metadata_in_summary(self):
        """Test that document metadata is properly included in summaries."""
        print("\nRunning test_document_metadata_in_summary...")
        query = "a lessee shall account for non-Ijarah"
        print(f"Query: {query}")
        results = self.retriever.retrieve(query)
        print(f"Retrieved {len(results)} documents.")
        
        if results:
            summaries = self.summarizer.summarize_findings({"default": results})
            summary = summaries.get("default", "")
            print(f"Generated summary: {summary}")
            
            # Verify that metadata elements are referenced in the summary
            for doc in results:
                self.assertIn(doc.document_type, summary)
                self.assertIn(doc.section_heading, summary)
        print("test_document_metadata_in_summary passed.")


def main():
    """Run the test suite."""
    unittest.main()

if __name__ == "__main__":
    main() 