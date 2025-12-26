"""
Test script for the Agentic RAG Chatbot
This script tests the core components without requiring a real OpenAI API key
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.dirname(__file__))

def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")
    
    try:
        from src.utils.vector_store import VectorStoreManager
        print("✓ VectorStoreManager imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import VectorStoreManager: {e}")
        return False
    
    try:
        from src.tools.retrieval_tool import RetrievalTool
        print("✓ RetrievalTool imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import RetrievalTool: {e}")
        return False
    
    try:
        from src.agents.rag_agent import AgenticRAGAgent
        print("✓ AgenticRAGAgent imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import AgenticRAGAgent: {e}")
        return False
    
    return True

def test_vector_store_structure():
    """Test vector store manager structure"""
    print("\nTesting VectorStoreManager structure...")
    
    from src.utils.vector_store import VectorStoreManager
    
    # Test initialization with defaults
    try:
        vsm = VectorStoreManager(
            documents_dir="data/documents",
            persist_directory="test_chroma_db"
        )
        print("✓ VectorStoreManager initialized with parameters")
        
        # Check methods exist
        assert hasattr(vsm, 'load_documents'), "Missing load_documents method"
        assert hasattr(vsm, 'split_documents'), "Missing split_documents method"
        assert hasattr(vsm, 'create_vectorstore'), "Missing create_vectorstore method"
        assert hasattr(vsm, 'get_retriever'), "Missing get_retriever method"
        print("✓ All required methods present")
        
        return True
    except Exception as e:
        print(f"✗ Failed to initialize VectorStoreManager: {e}")
        return False

def test_retrieval_tool_structure():
    """Test retrieval tool structure"""
    print("\nTesting RetrievalTool structure...")
    
    from src.tools.retrieval_tool import RetrievalTool
    
    try:
        # Create a mock retriever
        class MockRetriever:
            def get_relevant_documents(self, query):
                return []
        
        rt = RetrievalTool(MockRetriever())
        print("✓ RetrievalTool initialized")
        
        # Check methods exist
        assert hasattr(rt, 'as_tool'), "Missing as_tool method"
        print("✓ All required methods present")
        
        # Test as_tool method
        tool = rt.as_tool()
        assert tool.name == "knowledge_base_search", "Tool name mismatch"
        print("✓ Tool conversion works correctly")
        
        return True
    except Exception as e:
        print(f"✗ Failed to test RetrievalTool: {e}")
        return False

def test_agent_structure():
    """Test agent structure (without API key)"""
    print("\nTesting AgenticRAGAgent structure...")
    
    from src.agents.rag_agent import AgenticRAGAgent
    
    try:
        # Check class exists and has required methods
        assert hasattr(AgenticRAGAgent, 'chat'), "Missing chat method"
        assert hasattr(AgenticRAGAgent, 'reset_memory'), "Missing reset_memory method"
        assert hasattr(AgenticRAGAgent, 'get_conversation_history'), "Missing get_conversation_history method"
        print("✓ All required methods present in AgenticRAGAgent")
        
        return True
    except Exception as e:
        print(f"✗ Failed to test AgenticRAGAgent: {e}")
        return False

def test_file_structure():
    """Test that all required files exist"""
    print("\nTesting file structure...")
    
    required_files = [
        "chatbot.py",
        "requirements.txt",
        ".env.example",
        ".gitignore",
        "README.md",
        "src/__init__.py",
        "src/agents/__init__.py",
        "src/agents/rag_agent.py",
        "src/tools/__init__.py",
        "src/tools/retrieval_tool.py",
        "src/utils/__init__.py",
        "src/utils/vector_store.py",
        "data/documents/ai_basics.txt",
        "data/documents/rag_explained.txt",
        "data/documents/python_best_practices.txt"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
            print(f"✗ Missing: {file_path}")
        else:
            print(f"✓ Found: {file_path}")
    
    if missing_files:
        print(f"\n✗ {len(missing_files)} file(s) missing")
        return False
    else:
        print(f"\n✓ All {len(required_files)} required files present")
        return True

def main():
    """Run all tests"""
    print("="*60)
    print("Agentic RAG Chatbot - Component Tests")
    print("="*60)
    
    results = []
    
    # Run tests
    results.append(("File Structure", test_file_structure()))
    results.append(("Imports", test_imports()))
    results.append(("VectorStoreManager", test_vector_store_structure()))
    results.append(("RetrievalTool", test_retrieval_tool_structure()))
    results.append(("AgenticRAGAgent", test_agent_structure()))
    
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
        print("\n✓ All tests passed! The chatbot structure is correct.")
        print("\nNote: To run the actual chatbot, you need to:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Set up .env file with your OPENAI_API_KEY")
        print("3. Run: python chatbot.py")
        return 0
    else:
        print(f"\n✗ {total - passed} test(s) failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
