import sys
import os
from typing import List

# Add the src directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.agents.fas_retriever import FASDocument, FASRetriever

def test_fas_retriever_methods():
    """Test FASRetriever methods only."""

    retriever = FASRetriever()

    # Test 1: Basic query
    print("\nTest 1: Basic Query")
    results = retriever.retrieve(query="What is the definition of a lessee?")
    print_results(results)

def print_results(results: List[FASDocument]):
    """Print the results of the FASRetriever methods."""
    print(results)

if __name__ == "__main__":
    test_fas_retriever_methods()    
