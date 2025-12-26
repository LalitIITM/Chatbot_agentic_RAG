"""
Example: Programmatic Usage of Agentic RAG Chatbot
This demonstrates how to use the chatbot as a library
"""

import os
from dotenv import load_dotenv
from src.utils.vector_store import VectorStoreManager
from src.tools.retrieval_tool import RetrievalTool
from src.agents.rag_agent import AgenticRAGAgent

def example_basic_usage():
    """Basic example of using the chatbot programmatically"""
    print("="*60)
    print("Example 1: Basic Usage")
    print("="*60)
    
    # Load environment variables
    load_dotenv()
    
    # Initialize components
    print("\nInitializing components...")
    
    # 1. Set up vector store
    vector_store_manager = VectorStoreManager(
        documents_dir="data/documents",
        persist_directory="example_chroma_db"
    )
    
    # 2. Load and index documents
    documents = vector_store_manager.load_documents()
    vectorstore = vector_store_manager.create_vectorstore(documents)
    retriever = vector_store_manager.get_retriever()
    
    # 3. Create retrieval tool
    retrieval_tool = RetrievalTool(retriever)
    tools = [retrieval_tool.as_tool()]
    
    # 4. Initialize agent
    agent = AgenticRAGAgent(
        tools=tools,
        model_name="gpt-3.5-turbo",
        verbose=False  # Set to True to see agent reasoning
    )
    
    # 5. Ask questions
    print("\n" + "-"*60)
    questions = [
        "What is artificial intelligence?",
        "What are the benefits of RAG?",
        "What is agentic RAG?"
    ]
    
    for question in questions:
        print(f"\nQ: {question}")
        response = agent.chat(question)
        print(f"A: {response}")
        print("-"*60)

def example_with_custom_documents():
    """Example showing how to add custom documents"""
    print("\n" + "="*60)
    print("Example 2: Adding Custom Documents")
    print("="*60)
    
    from langchain.schema import Document
    
    load_dotenv()
    
    # Initialize vector store
    vector_store_manager = VectorStoreManager(
        persist_directory="custom_chroma_db"
    )
    
    # Create custom documents
    custom_docs = [
        Document(
            page_content="The capital of France is Paris. It is known for the Eiffel Tower.",
            metadata={"source": "geography", "topic": "France"}
        ),
        Document(
            page_content="Python is a programming language created by Guido van Rossum.",
            metadata={"source": "programming", "topic": "Python"}
        )
    ]
    
    print("\nAdding custom documents...")
    vectorstore = vector_store_manager.create_vectorstore(custom_docs)
    retriever = vector_store_manager.get_retriever()
    
    # Create agent with custom knowledge
    retrieval_tool = RetrievalTool(retriever)
    agent = AgenticRAGAgent(
        tools=[retrieval_tool.as_tool()],
        verbose=False
    )
    
    # Ask questions about custom content
    print("\n" + "-"*60)
    response = agent.chat("What is the capital of France?")
    print(f"Q: What is the capital of France?")
    print(f"A: {response}")
    print("-"*60)

def example_conversation_with_memory():
    """Example showing conversation memory"""
    print("\n" + "="*60)
    print("Example 3: Conversation with Memory")
    print("="*60)
    
    load_dotenv()
    
    # Initialize components
    vector_store_manager = VectorStoreManager(documents_dir="data/documents")
    documents = vector_store_manager.load_documents()
    vectorstore = vector_store_manager.create_vectorstore(documents)
    retriever = vector_store_manager.get_retriever()
    
    retrieval_tool = RetrievalTool(retriever)
    agent = AgenticRAGAgent(
        tools=[retrieval_tool.as_tool()],
        verbose=False
    )
    
    # Multi-turn conversation
    print("\n" + "-"*60)
    conversation = [
        "What is RAG?",
        "How does it work?",  # Follow-up question using context
        "What are its benefits?"  # Another follow-up
    ]
    
    for question in conversation:
        print(f"\nQ: {question}")
        response = agent.chat(question)
        print(f"A: {response[:200]}...")  # Show first 200 chars
        print("-"*60)
    
    # Show conversation history
    print("\n📝 Full Conversation History:")
    print(agent.get_conversation_history())

def example_similarity_search():
    """Example of direct similarity search"""
    print("\n" + "="*60)
    print("Example 4: Direct Similarity Search")
    print("="*60)
    
    load_dotenv()
    
    # Initialize vector store
    vector_store_manager = VectorStoreManager(documents_dir="data/documents")
    documents = vector_store_manager.load_documents()
    vectorstore = vector_store_manager.create_vectorstore(documents)
    
    # Perform direct similarity search
    print("\nSearching for: 'machine learning applications'")
    results = vector_store_manager.similarity_search(
        "machine learning applications",
        k=3
    )
    
    print(f"\nFound {len(results)} relevant chunks:")
    for i, doc in enumerate(results, 1):
        print(f"\n--- Result {i} ---")
        print(f"Content: {doc.page_content[:200]}...")
        print(f"Source: {doc.metadata.get('source', 'Unknown')}")

def main():
    """Run all examples"""
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY not found")
        print("\nPlease create a .env file with your OpenAI API key:")
        print("OPENAI_API_KEY=your_key_here")
        return
    
    print("🤖 Agentic RAG Chatbot - Programmatic Examples\n")
    
    try:
        # Run examples
        # Uncomment the examples you want to run
        
        example_basic_usage()
        # example_with_custom_documents()
        # example_conversation_with_memory()
        # example_similarity_search()
        
        print("\n✅ Examples completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        print("\nMake sure you have:")
        print("1. Installed dependencies: pip install -r requirements.txt")
        print("2. Set up .env file with OPENAI_API_KEY")

if __name__ == "__main__":
    main()
