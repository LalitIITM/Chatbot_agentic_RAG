"""
Query Cache Manager
Handles caching of query-response pairs to reduce LLM API calls
"""

import os
import time
from typing import Optional, Dict, Any
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document


class QueryCache:
    """Manages query-response caching using semantic similarity"""
    
    def __init__(
        self,
        persist_directory: str = "query_cache_db",
        embedding_model: str = "text-embedding-ada-002",
        similarity_threshold: float = 0.95,
        cache_ttl: int = 86400,  # 24 hours in seconds
        enabled: bool = True
    ):
        """
        Initialize the query cache
        
        Args:
            persist_directory: Directory to persist the cache
            embedding_model: OpenAI embedding model to use
            similarity_threshold: Minimum similarity score to consider a cache hit (0-1)
            cache_ttl: Time-to-live for cache entries in seconds (default: 24 hours)
            enabled: Whether caching is enabled
        """
        self.persist_directory = persist_directory
        self.similarity_threshold = similarity_threshold
        self.cache_ttl = cache_ttl
        self.enabled = enabled
        self.embeddings = None
        self.cache_store: Optional[Chroma] = None
        
        if self.enabled:
            self.embeddings = OpenAIEmbeddings(model=embedding_model)
            self._initialize_cache()
    
    def _initialize_cache(self):
        """Initialize or load the cache store"""
        if os.path.exists(self.persist_directory):
            print(f"Loading existing query cache from {self.persist_directory}")
            self.cache_store = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings,
                collection_name="query_cache"
            )
        else:
            print(f"Creating new query cache at {self.persist_directory}")
            # Create empty collection - ChromaDB will initialize properly
            self.cache_store = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings,
                collection_name="query_cache"
            )
    
    def get(self, query: str, session_id: str = "default") -> Optional[str]:
        """
        Get a cached response for a similar query
        
        Args:
            query: The user's query
            session_id: Session identifier for context-aware caching
            
        Returns:
            Cached response if found and valid, None otherwise
        """
        if not self.enabled or self.cache_store is None:
            return None
        
        try:
            # Search for similar queries
            results = self.cache_store.similarity_search_with_score(
                query,
                k=1
            )
            
            if not results:
                return None
            
            doc, score = results[0]
            
            # Convert ChromaDB's L2 distance to similarity score
            # ChromaDB returns L2 (Euclidean) distance where:
            # - Distance of 0 = perfect match (same vectors)
            # - Larger distance = less similar vectors
            # We convert to similarity score (0-1) where 1 = perfect match:
            # Formula: similarity = 1 / (1 + distance)
            # - distance=0 → similarity=1.0 (perfect match)
            # - distance=1 → similarity=0.5
            # - distance=10 → similarity=0.09
            similarity = 1 / (1 + score)
            
            # Check if similarity meets threshold
            if similarity < self.similarity_threshold:
                return None
            
            # Check if cache entry is still valid (not expired)
            timestamp = doc.metadata.get("timestamp", 0)
            if time.time() - timestamp > self.cache_ttl:
                print(f"Cache hit but expired (age: {int(time.time() - timestamp)}s)")
                return None
            
            response = doc.metadata.get("response")
            if response:
                print(f"✓ Cache HIT (similarity: {similarity:.3f})")
                return response
            
            return None
            
        except Exception as e:
            print(f"Error retrieving from cache: {str(e)}")
            return None
    
    def set(
        self,
        query: str,
        response: str,
        session_id: str = "default",
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Store a query-response pair in the cache
        
        Args:
            query: The user's query
            response: The assistant's response
            session_id: Session identifier
            metadata: Additional metadata to store
        """
        if not self.enabled or self.cache_store is None:
            return
        
        try:
            # Create metadata with timestamp
            cache_metadata = {
                "response": response,
                "timestamp": time.time(),
                "session_id": session_id
            }
            
            # Add any additional metadata
            if metadata:
                cache_metadata.update(metadata)
            
            # Create document
            doc = Document(
                page_content=query,
                metadata=cache_metadata
            )
            
            # Add to cache store
            self.cache_store.add_documents([doc])
            print(f"✓ Cached query-response pair")
            
        except Exception as e:
            print(f"Error storing in cache: {str(e)}")
    
    def clear(self):
        """Clear all cache entries"""
        if not self.enabled or self.cache_store is None:
            return
        
        try:
            # Delete and reinitialize
            self.cache_store.delete_collection()
            self._initialize_cache()
            print("✓ Cache cleared")
        except Exception as e:
            print(f"Error clearing cache: {str(e)}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        if not self.enabled or self.cache_store is None:
            return {"enabled": False}
        
        try:
            collection = self.cache_store._collection
            count = collection.count()
            
            return {
                "enabled": True,
                "total_entries": count,
                "similarity_threshold": self.similarity_threshold,
                "cache_ttl_hours": self.cache_ttl / 3600
            }
        except Exception as e:
            return {
                "enabled": True,
                "error": str(e)
            }
