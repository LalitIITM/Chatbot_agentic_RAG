"""
Flask Web Application for Agentic RAG Chatbot
Provides a modern ChatGPT-like web interface
"""

import os
import sys
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from src.utils.vector_store import VectorStoreManager
from src.tools.retrieval_tool import RetrievalTool
from src.agents.rag_agent import AgenticRAGAgent

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Security: Require SECRET_KEY to be set explicitly
secret_key = os.getenv('SECRET_KEY')
if not secret_key:
    raise ValueError(
        "SECRET_KEY not found in environment variables. "
        "Please set SECRET_KEY in your .env file for session security."
    )
app.config['SECRET_KEY'] = secret_key

# Global chatbot instance
chatbot_agent = None


def initialize_chatbot(documents_dir: str = "data/documents"):
    """
    Initialize the chatbot instance
    
    Args:
        documents_dir: Directory containing documents to index
    """
    global chatbot_agent
    
    # Verify API key
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError(
            "OPENAI_API_KEY not found in environment variables. "
            "Please create a .env file with your OpenAI API key."
        )
    
    print("🤖 Initializing Agentic RAG Chatbot...")
    
    # Initialize vector store
    print("\n📚 Setting up knowledge base...")
    vector_store_manager = VectorStoreManager(documents_dir=documents_dir)
    
    # Load and index documents
    documents = vector_store_manager.load_documents()
    vectorstore = vector_store_manager.create_vectorstore(documents)
    retriever = vector_store_manager.get_retriever()
    
    # Create retrieval tool
    print("\n🔧 Creating agent tools...")
    retrieval_tool = RetrievalTool(retriever)
    tools = [retrieval_tool.as_tool()]
    
    # Initialize agent
    print("\n🧠 Initializing agent...")
    model_name = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    chatbot_agent = AgenticRAGAgent(
        tools=tools,
        model_name=model_name,
        verbose=False  # Disable verbose output for web interface
    )
    
    print("\n✅ Chatbot initialized successfully!")


@app.route('/')
def index():
    """Render the main chat interface"""
    return render_template('index.html')


@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Handle chat messages from the frontend
    
    Expected JSON payload:
    {
        "message": "user's question"
    }
    
    Returns:
    {
        "response": "assistant's response",
        "success": true/false,
        "error": "error message if any"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({
                'success': False,
                'error': 'No message provided'
            }), 400
        
        user_message = data['message'].strip()
        
        if not user_message:
            return jsonify({
                'success': False,
                'error': 'Empty message'
            }), 400
        
        # Check if chatbot is initialized
        if chatbot_agent is None:
            return jsonify({
                'success': False,
                'error': 'Chatbot not initialized. Please check server logs.'
            }), 503
        
        # Get response from chatbot
        response = chatbot_agent.chat(user_message)
        
        return jsonify({
            'success': True,
            'response': response
        })
        
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Error processing message: {str(e)}'
        }), 500


@app.route('/api/reset', methods=['POST'])
def reset():
    """
    Reset the conversation history
    
    Returns:
    {
        "success": true/false,
        "message": "status message"
    }
    """
    try:
        # Check if chatbot is initialized
        if chatbot_agent is None:
            return jsonify({
                'success': False,
                'error': 'Chatbot not initialized. Please check server logs.'
            }), 503
        
        chatbot_agent.reset_memory()
        return jsonify({
            'success': True,
            'message': 'Conversation history cleared'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error resetting conversation: {str(e)}'
        }), 500


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'chatbot_initialized': chatbot_agent is not None
    })


def main():
    """Main entry point for the Flask application"""
    try:
        # Initialize the chatbot
        initialize_chatbot()
        
        # Run the Flask app
        port = int(os.getenv('PORT', 5000))
        host = os.getenv('FLASK_HOST', '127.0.0.1')  # Default to localhost for security
        debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
        
        print(f"\n🌐 Starting web server on http://{host}:{port}")
        print("Press Ctrl+C to stop the server\n")
        
        app.run(host=host, port=port, debug=debug)
        
    except Exception as e:
        print(f"\n❌ Failed to start application: {str(e)}")
        print("\nMake sure you have:")
        print("1. Created a .env file with your OPENAI_API_KEY")
        print("2. Installed all dependencies: pip install -r requirements.txt")
        sys.exit(1)


if __name__ == '__main__':
    main()
