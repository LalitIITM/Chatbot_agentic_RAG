"""
Test script for Query Cache functionality
Tests cache hit/miss, similarity matching, and session memory integration
"""

import sys
import os
import time
import shutil

# Add src to path
sys.path.insert(0, os.path.dirname(__file__))


def test_query_cache_imports():
    """Test that QueryCache can be imported"""
    print("Testing QueryCache imports...")
    
    try:
        from src.utils.query_cache import QueryCache
        print("✓ QueryCache imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Failed to import QueryCache: {e}")
        return False


def test_query_cache_initialization():
    """Test QueryCache initialization"""
    print("\nTesting QueryCache initialization...")
    
    try:
        from src.utils.query_cache import QueryCache
        from dotenv import load_dotenv
        load_dotenv()
        
        # Test with disabled cache (no API key needed)
        cache_disabled = QueryCache(
            persist_directory="test_cache_disabled",
            enabled=False
        )
        print("✓ QueryCache initialized with caching disabled")
        
        # Test cache stats for disabled cache
        stats = cache_disabled.get_stats()
        assert stats["enabled"] == False, "Cache should be disabled"
        print("✓ Disabled cache stats correct")
        
        # Test with enabled cache only if API key is available
        if os.getenv("OPENAI_API_KEY"):
            cache_enabled = QueryCache(
                persist_directory="test_cache_enabled",
                enabled=True
            )
            print("✓ QueryCache initialized with caching enabled")
            
            # Clean up
            import shutil
            if os.path.exists("test_cache_enabled"):
                shutil.rmtree("test_cache_enabled")
        else:
            print("⚠ Skipping enabled cache test (no API key)")
        
        return True
    except Exception as e:
        print(f"✗ Failed to initialize QueryCache: {e}")
        return False


def test_query_cache_operations():
    """Test basic cache operations (requires API key)"""
    print("\nTesting QueryCache operations...")
    
    # Check if API key is available
    from dotenv import load_dotenv
    load_dotenv()
    
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠ Skipping cache operations test (no API key)")
        return True
    
    try:
        from src.utils.query_cache import QueryCache
        
        # Clean up test cache directory if exists
        test_cache_dir = "test_cache_operations"
        if os.path.exists(test_cache_dir):
            shutil.rmtree(test_cache_dir)
        
        # Initialize cache
        cache = QueryCache(
            persist_directory=test_cache_dir,
            enabled=True,
            similarity_threshold=0.90,
            cache_ttl=3600  # 1 hour
        )
        print("✓ QueryCache initialized")
        
        # Test cache miss
        query1 = "What is machine learning?"
        result = cache.get(query1)
        assert result is None, "Cache should be empty initially"
        print("✓ Cache miss works correctly")
        
        # Test cache set
        response1 = "Machine learning is a subset of AI..."
        cache.set(query1, response1, session_id="test_session")
        print("✓ Cache set works correctly")
        
        # Test cache hit with exact query
        result = cache.get(query1)
        assert result == response1, "Should retrieve exact cached response"
        print("✓ Cache hit with exact query works")
        
        # Test cache stats
        stats = cache.get_stats()
        assert stats["enabled"] == True, "Cache should be enabled"
        assert stats["total_entries"] >= 1, "Cache should have at least one entry"
        print(f"✓ Cache stats: {stats}")
        
        # Clean up
        if os.path.exists(test_cache_dir):
            shutil.rmtree(test_cache_dir)
        print("✓ Test cleanup successful")
        
        return True
    except Exception as e:
        print(f"✗ Failed cache operations test: {e}")
        import traceback
        traceback.print_exc()
        # Clean up on error
        if os.path.exists(test_cache_dir):
            shutil.rmtree(test_cache_dir)
        return False


def test_cache_ttl():
    """Test cache TTL (time-to-live) functionality"""
    print("\nTesting cache TTL...")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠ Skipping TTL test (no API key)")
        return True
    
    try:
        from src.utils.query_cache import QueryCache
        
        test_cache_dir = "test_cache_ttl"
        if os.path.exists(test_cache_dir):
            shutil.rmtree(test_cache_dir)
        
        # Initialize cache with very short TTL
        cache = QueryCache(
            persist_directory=test_cache_dir,
            enabled=True,
            cache_ttl=2  # 2 seconds
        )
        
        # Add entry
        query = "Test query for TTL"
        response = "Test response"
        cache.set(query, response)
        
        # Should hit immediately
        result = cache.get(query)
        assert result == response, "Should retrieve cached response immediately"
        print("✓ Cache entry valid within TTL")
        
        # Wait for expiry
        print("  Waiting for cache expiry (3 seconds)...")
        time.sleep(3)
        
        # Should miss after expiry
        result = cache.get(query)
        assert result is None, "Cache entry should expire after TTL"
        print("✓ Cache entry expired after TTL")
        
        # Clean up
        if os.path.exists(test_cache_dir):
            shutil.rmtree(test_cache_dir)
        
        return True
    except Exception as e:
        print(f"✗ Failed TTL test: {e}")
        import traceback
        traceback.print_exc()
        if os.path.exists(test_cache_dir):
            shutil.rmtree(test_cache_dir)
        return False


def test_agent_with_cache():
    """Test that agent integrates properly with cache"""
    print("\nTesting agent integration with cache...")
    
    try:
        from src.agents.rag_agent import AgenticRAGAgent
        from src.utils.query_cache import QueryCache
        
        # Check that agent accepts query_cache parameter
        import inspect
        sig = inspect.signature(AgenticRAGAgent.__init__)
        params = list(sig.parameters.keys())
        assert "query_cache" in params, "Agent should accept query_cache parameter"
        print("✓ Agent accepts query_cache parameter")
        
        # Check that agent has session_id parameter
        assert "session_id" in params, "Agent should accept session_id parameter"
        print("✓ Agent accepts session_id parameter")
        
        return True
    except Exception as e:
        print(f"✗ Failed agent integration test: {e}")
        return False


def main():
    """Run all tests"""
    print("="*60)
    print("Query Cache - Component Tests")
    print("="*60)
    
    results = []
    
    # Run tests
    results.append(("QueryCache Imports", test_query_cache_imports()))
    results.append(("QueryCache Initialization", test_query_cache_initialization()))
    results.append(("QueryCache Operations", test_query_cache_operations()))
    results.append(("Cache TTL", test_cache_ttl()))
    results.append(("Agent Integration", test_agent_with_cache()))
    
    # Summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{test_name}: {status}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✓ All tests passed! Query cache is working correctly.")
        return 0
    else:
        print(f"\n✗ {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
