"""
Test script for FAS Retriever agent.
"""

import sys
import os
from typing import List

# Add the src directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.agents.ss_retiever import (SSDocument, SSRetriever)

def test_ss_retriever_methods():
    """Test SSRetriever methods only."""
    print("\n=== Testing FASRetriever Methods ===")
    retriever = SSRetriever()

    # Test 1: Basic query
    print("\nTest 1: Basic Query")
    results = retriever.retrieve(query="What is Musharaka financing?", top_n=2)
    print_results(results)

    # Test 2: Query with document type filter
    print("\nTest 2: Query with Document Type Filter")
    results = retriever.retrieve(
        query="Payment terms and conditions",
        document_types="ss_28_Murabaha_Deferred_Payment_Sales",
        top_n=2
    )
    print_results(results)

    # Test 3: Query with multiple document types
    print("\nTest 3: Query with Multiple Document Types")
    results = retriever.retrieve(
        query="Contract termination",
        document_types=["SS_8_Murabahah"],
        top_n=2
    )
    print_results(results)

    # Test 4: Query with section heading
    print("\nTest 4: Query with Section Heading")
    results = retriever.retrieve(
        query="Mudaraba",
        top_n=2
    )
    print_results(results)

    # Test 5: Keyword-based search
    print("\nTest 5: Keyword-based Search")
    keywords = ["profit", "loss", "sharing", "Musharaka"]
    results = retriever.retrieve_by_keywords(
        keywords=keywords,
        document_types="ss_4_Musharaka",
        top_n=2
    )
    print_results(results)

    # Test 6: List available document types
    print("\nTest 6: Available Document Types")
    doc_types = retriever.get_available_document_types()
    print("Available ss Document Types:")
    for doc_type in doc_types:
        print(f"- {doc_type}")

def print_results(results: List[SSDocument]):
    if not results:
        print("No results found.")
        return
    print("\n=== Search Results ===")
    for i, doc in enumerate(results, 1):
        print(f"\nResult {i}:")
        print(f"Relevance Score: {doc.relevance_score:.4f}")
        print(f"Document Type: {doc.document_type}")
        print(f"Section: {doc.section_heading}")
        print(f"Source: {doc.source_filename}")
        print(f"Chunk: {doc.chunk_index}/{doc.total_chunks}")
        print("Content:")
        print(f"{doc.text[:300]}...")
        print("-" * 40)
    print("\n=== End of Results ===")

if __name__ == "__main__":
    test_ss_retriever_methods()