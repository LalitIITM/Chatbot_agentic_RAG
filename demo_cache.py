"""
Manual Test/Demo Script for Query Cache
This script demonstrates the query caching functionality
Requires OPENAI_API_KEY to be set in .env
"""

import os
import sys
import time
from dotenv import load_dotenv

# Add src to path
sys.path.insert(0, os.path.dirname(__file__))

def demo_query_cache():
    """Demonstrate query cache functionality"""
    load_dotenv()
    
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY not found in environment")
        print("Please create a .env file with your OpenAI API key")
        return False
    
    print("="*60)
    print("Query Cache Manual Test/Demo")
    print("="*60)
    
    try:
        from src.utils.query_cache import QueryCache
        import shutil
        
        # Clean up test cache if exists
        test_cache_dir = "demo_cache"
        if os.path.exists(test_cache_dir):
            shutil.rmtree(test_cache_dir)
        
        print("\n1. Initializing Query Cache...")
        cache = QueryCache(
            persist_directory=test_cache_dir,
            enabled=True,
            similarity_threshold=0.90,  # Lower threshold for demo
            cache_ttl=3600  # 1 hour
        )
        print("   ✓ Cache initialized")
        
        # Test query-response pairs
        queries = [
            ("What is machine learning?", "Machine learning is a subset of AI that enables systems to learn from data."),
            ("Explain deep learning", "Deep learning is a subset of machine learning using neural networks with many layers."),
            ("What is RAG?", "RAG stands for Retrieval-Augmented Generation, combining retrieval with generation.")
        ]
        
        print("\n2. Adding query-response pairs to cache...")
        for query, response in queries:
            cache.set(query, response, session_id="demo_session")
            print(f"   ✓ Cached: '{query[:50]}...'")
        
        print("\n3. Testing exact query match (cache hit)...")
        result = cache.get("What is machine learning?")
        if result:
            print(f"   ✓ Cache HIT! Retrieved: '{result[:60]}...'")
        else:
            print("   ✗ Cache MISS (unexpected)")
        
        print("\n4. Testing similar query (semantic matching)...")
        similar_queries = [
            "What's machine learning?",  # Very similar
            "Can you explain machine learning?",  # Similar
            "Tell me about ML",  # Related but different
        ]
        
        for sq in similar_queries:
            result = cache.get(sq)
            if result:
                print(f"   ✓ Query: '{sq}'")
                print(f"     Cache HIT! (similarity >= 0.90)")
            else:
                print(f"   ○ Query: '{sq}'")
                print(f"     Cache MISS (similarity < 0.90)")
        
        print("\n5. Testing cache stats...")
        stats = cache.get_stats()
        print(f"   Enabled: {stats['enabled']}")
        print(f"   Total entries: {stats['total_entries']}")
        print(f"   Similarity threshold: {stats['similarity_threshold']}")
        print(f"   TTL: {stats['cache_ttl_hours']:.1f} hours")
        
        print("\n6. Testing cache with completely different query...")
        result = cache.get("What is the weather today?")
        if result:
            print(f"   ✗ Unexpected cache hit")
        else:
            print(f"   ✓ Cache MISS (as expected for unrelated query)")
        
        print("\n7. Cleaning up test cache...")
        if os.path.exists(test_cache_dir):
            shutil.rmtree(test_cache_dir)
        print("   ✓ Cleanup complete")
        
        print("\n" + "="*60)
        print("✓ Demo completed successfully!")
        print("="*60)
        print("\nKey Benefits:")
        print("  • Semantic matching finds similar queries (not just exact)")
        print("  • Reduces LLM API calls = Cost savings")
        print("  • Faster response times for cached queries")
        print("  • Configurable threshold and TTL")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error during demo: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def demo_with_agent():
    """Demonstrate cache integration with agent"""
    load_dotenv()
    
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠ Skipping agent demo (no API key)")
        return True
    
    print("\n" + "="*60)
    print("Agent Integration Demo")
    print("="*60)
    
    try:
        from src.agents.rag_agent import AgenticRAGAgent
        from src.utils.query_cache import QueryCache
        from src.utils.vector_store import VectorStoreManager
        from src.tools.retrieval_tool import RetrievalTool
        import shutil
        
        print("\nThis demo would:")
        print("  1. Initialize vector store with documents")
        print("  2. Create retrieval tool")
        print("  3. Initialize agent with query cache enabled")
        print("  4. Ask a question (calls LLM)")
        print("  5. Ask similar question (cache hit - no LLM call!)")
        print("  6. Show cost savings")
        print("\n⚠ Skipping full demo to avoid API costs")
        print("  To run full demo, uncomment the code in demo_with_agent()")
        
        # Uncomment below to run full demo (will incur API costs)
        """
        # Initialize components
        print("\n1. Initializing components...")
        vector_store_manager = VectorStoreManager()
        docs = vector_store_manager.load_documents()
        vectorstore = vector_store_manager.create_vectorstore(docs)
        retriever = vector_store_manager.get_retriever()
        
        retrieval_tool = RetrievalTool(retriever)
        
        cache = QueryCache(enabled=True)
        
        agent = AgenticRAGAgent(
            tools=[retrieval_tool.as_tool()],
            query_cache=cache,
            verbose=False
        )
        
        print("\n2. First query (will call LLM)...")
        start = time.time()
        response1 = agent.chat("What is RAG?")
        time1 = time.time() - start
        print(f"   Response: {response1[:100]}...")
        print(f"   Time: {time1:.2f}s")
        
        print("\n3. Similar query (should hit cache)...")
        start = time.time()
        response2 = agent.chat("What's RAG?")
        time2 = time.time() - start
        print(f"   Response: {response2[:100]}...")
        print(f"   Time: {time2:.2f}s")
        print(f"   ✓ Speedup: {time1/time2:.1f}x faster!")
        """
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error during agent demo: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all demos"""
    success = True
    
    # Run cache demo
    success = demo_query_cache() and success
    
    # Run agent demo
    success = demo_with_agent() and success
    
    if success:
        print("\n✓ All demos completed successfully!")
        return 0
    else:
        print("\n✗ Some demos failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
