"""
FAS Document Retriever Agent
Purpose: Retrieves relevant sections from FAS documents based on queries.
"""

from typing import List, Dict, Optional, Union
from pydantic import BaseModel
from pinecone import Pinecone
from ..core.config import settings
import openai
from openai import OpenAI

class SSDocument(BaseModel):
    """Model for SS document chunks."""
    id: str
    text: str
    relevance_score: float
    document_type: str
    section_heading: str
    source_filename: str
    chunk_index: int
    total_chunks: int
    metadata: Optional[Dict] = None



class SSRetriever:
    def __init__(self):
        """Initialize the SS Retriever agent."""
        # Initialize Pinecone client
        self.pc = Pinecone(
            api_key=settings.PINECONE_API_KEY,
            environment=settings.PINECONE_ENVIRONMENT
        )
        
        # Get the SS index
        self.index = self.pc.Index(settings.PINECONE_INDEX_SS)
        
        # Verify index connection
        try:
            stats = self.index.describe_index_stats()
            print(f"Connected to Pinecone index. Stats: {stats}")
        except Exception as e:
            print(f"Error connecting to Pinecone index: {e}")
            raise

    def embed_query(self, query: str) -> list:
        """
        Embed a query string into a vector using OpenAI's text-embedding-3-small model.
        """
        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        response = client.embeddings.create(input=query, model="text-embedding-3-small")
        return response.data[0].embedding

    def _format_search_results(self, results: List[Dict]) -> List[SSDocument]:
        """
        Format Pinecone search results into SSDocument objects.
        
        Args:
            results: Raw search results from Pinecone
            
        Returns:
            List of formatted SSDocument objects
        """
        formatted_results = []
        for match in results:
            metadata = match.get('metadata', {})
            
            # Create SSDocument object with new structure
            doc = SSDocument(
                id=match.get('id', ''),
                text=metadata.get('text', ''),
                relevance_score=match.get('score', 0.0),
                document_type=metadata.get('document_type', ''),
                section_heading=metadata.get('section_heading', ''),
                source_filename=metadata.get('source_filename', ''),
                chunk_index=metadata.get('chunk_index', 0),
                total_chunks=metadata.get('total_chunks', 0),
                metadata=metadata
            )
            formatted_results.append(doc)
        
        return formatted_results

    def retrieve(
        self,
        query: str,
        top_n: int = 5,
        document_types: Optional[Union[str, List[str]]] = None,
        section_heading: Optional[str] = None,
        namespace: str = "default"
    ) -> List[SSDocument]:
        """
        Retrieve relevant SS document chunks based on the query.
        
        Args:
            query: Search query
            top_n: Number of top results to return
            document_types: Optional document type(s) to filter by
            section_heading: Optional section heading to filter by
            namespace: Namespace to search in (defaults to "default")
            
        Returns:
            List of SSDocument objects containing relevant chunks
        """
        try:
            query_vector = self.embed_query(query)
            
            # Build filter criteria
            filter_criteria = {}
            if document_types:
                if isinstance(document_types, str):
                    filter_criteria["document_type"] = {"$eq": document_types}
                else:
                    filter_criteria["document_type"] = {"$in": document_types}
            
            if section_heading:
                if filter_criteria:
                    filter_criteria = {
                        "$and": [
                            filter_criteria,
                            {"section_heading": {"$eq": section_heading}}
                        ]
                    }
                else:
                    filter_criteria["section_heading"] = {"$eq": section_heading}

            search_results = self.index.query(
                vector=query_vector,
                top_k=top_n,
                include_metadata=True,
                filter=filter_criteria if filter_criteria else None,
                namespace=namespace
            )
            
            return self._format_search_results(search_results.matches)
        except Exception as e:
            print(f"Error retrieving documents: {e}")
            return []

    def retrieve_by_keywords(
        self,
        keywords: List[str],
        top_n: int = 5,
        document_types: Optional[Union[str, List[str]]] = None,
        section_heading: Optional[str] = None,
        namespace: str = "default"
    ) -> List[SSDocument]:
        """
        Retrieve documents using a list of keywords.
        
        Args:
            keywords: List of search keywords
            top_n: Number of top results to return
            document_types: Optional document type(s) to filter by
            section_heading: Optional section heading to filter by
            namespace: Namespace to search in (defaults to "default")
            
        Returns:
            List of SSDocument objects containing relevant chunks
        """
        query = " ".join(keywords)
        return self.retrieve(
            query=query,
            top_n=top_n,
            document_types=document_types,
            section_heading=section_heading,
            namespace=namespace
        )

    def get_available_document_types(self) -> List[str]:
        """Return list of available SS document types."""
        return [
            "SS_8_Murabahah",
            "SS_9_Ijarah_Ijarah_Muntahia_Bittamleek",
            "SS_10_Salam_Parallel_Salam",
            "SS_12_Musharakah"
        ]