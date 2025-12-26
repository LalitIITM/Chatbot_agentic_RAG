"""
Agentic RAG Chatbot - Main Application
A chatbot implementation using agentic RAG with reasoning capabilities
"""

import os
import sys
from dotenv import load_dotenv
from src.utils.vector_store import VectorStoreManager
from src.tools.retrieval_tool import RetrievalTool
from src.agents.rag_agent import AgenticRAGAgent


class AgenticRAGChatbot:
    """Main chatbot application"""
    
    def __init__(self, documents_dir: str = "data/documents"):
        """
        Initialize the chatbot
        
        Args:
            documents_dir: Directory containing documents to index
        """
        load_dotenv()
        
        # Verify API key
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError(
                "OPENAI_API_KEY not found in environment variables. "
                "Please create a .env file with your OpenAI API key."
            )
        
        print("🤖 Initializing Agentic RAG Chatbot...")
        
        # Initialize vector store
        print("\n📚 Setting up knowledge base...")
        self.vector_store_manager = VectorStoreManager(
            documents_dir=documents_dir
        )
        
        # Load and index documents
        documents = self.vector_store_manager.load_documents()
        self.vectorstore = self.vector_store_manager.create_vectorstore(documents)
        retriever = self.vector_store_manager.get_retriever()
        
        # Create retrieval tool
        print("\n🔧 Creating agent tools...")
        retrieval_tool = RetrievalTool(retriever)
        tools = [retrieval_tool.as_tool()]
        
        # Initialize agent
        print("\n🧠 Initializing agent...")
        model_name = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
        self.agent = AgenticRAGAgent(
            tools=tools,
            model_name=model_name,
            verbose=True
        )
        
        print("\n✅ Chatbot initialized successfully!")
    
    def chat(self, message: str) -> str:
        """Send a message to the chatbot"""
        return self.agent.chat(message)
    
    def run_cli(self):
        """Run the chatbot in CLI mode"""
        print("\n" + "="*60)
        print("🤖 Agentic RAG Chatbot")
        print("="*60)
        print("\nCommands:")
        print("  - Type your question to chat")
        print("  - 'history' - Show conversation history")
        print("  - 'reset' - Clear conversation history")
        print("  - 'quit' or 'exit' - Exit the chatbot")
        print("\n" + "="*60 + "\n")
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['quit', 'exit']:
                    print("\n👋 Goodbye!")
                    break
                
                if user_input.lower() == 'reset':
                    self.agent.reset_memory()
                    print("\n🔄 Conversation history cleared.\n")
                    continue
                
                if user_input.lower() == 'history':
                    history = self.agent.get_conversation_history()
                    if history:
                        print("\n📝 Conversation History:")
                        print("-" * 60)
                        print(history)
                        print("-" * 60 + "\n")
                    else:
                        print("\n📝 No conversation history yet.\n")
                    continue
                
                # Get response from agent
                print("\n🤖 Assistant: ", end="", flush=True)
                response = self.chat(user_input)
                print(response)
                print()
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {str(e)}\n")


def main():
    """Main entry point"""
    try:
        chatbot = AgenticRAGChatbot()
        chatbot.run_cli()
    except Exception as e:
        print(f"\n❌ Failed to initialize chatbot: {str(e)}")
        print("\nMake sure you have:")
        print("1. Created a .env file with your OPENAI_API_KEY")
        print("2. Installed all dependencies: pip install -r requirements.txt")
        sys.exit(1)


if __name__ == "__main__":
    main()
