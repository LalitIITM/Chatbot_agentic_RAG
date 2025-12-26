# 🤖 Agentic RAG Chatbot

An intelligent chatbot built with **Agentic RAG** (Retrieval-Augmented Generation) that combines reasoning capabilities with knowledge retrieval to provide accurate, context-aware responses.

**✨ Now with a modern ChatGPT-like web interface!** 🌐

## 🌟 Features

- **Modern Web Interface**: ChatGPT-inspired UI with dark theme and responsive design 🎨
- **Agentic Behavior**: The chatbot can reason about what information it needs and decide when to use retrieval tools
- **RAG Pipeline**: Combines retrieval from a knowledge base with language model generation
- **Conversation Memory**: Maintains context across the conversation
- **Vector Search**: Uses ChromaDB and OpenAI embeddings for semantic search
- **Extensible Tool System**: Easy to add new tools and capabilities
- **Interactive CLI**: User-friendly command-line interface (legacy mode)

## 🏗️ Architecture

The system consists of several key components:

1. **Vector Store Manager**: Handles document loading, chunking, and embedding
2. **Retrieval Tool**: Searches the knowledge base for relevant information
3. **Agentic RAG Agent**: Uses reasoning to decide when and how to use tools
4. **Chatbot Interface**: Manages user interaction and conversation flow

## 📋 Prerequisites

- Python 3.8 or higher
- OpenAI API key

## 🚀 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/LalitIITM/Chatbot_agentic_RAG.git
   cd Chatbot_agentic_RAG
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   - Copy `.env.example` to `.env`
   - Configure required settings in the `.env` file:
     ```
     OPENAI_API_KEY=your_openai_api_key_here
     SECRET_KEY=your-random-secret-key-here
     ```
   - Generate a secure SECRET_KEY with:
     ```bash
     python -c "import secrets; print(secrets.token_hex(32))"
     ```

## 📖 Usage

### Option 1: Web Interface (Recommended) 🌐

Start the web application with a modern ChatGPT-like interface:
```bash
python app.py
```

Then open your browser and navigate to:
```
http://localhost:5000
```

**Features:**
- Modern, ChatGPT-inspired interface with dark theme
- Real-time chat interactions
- Conversation history management
- Responsive design for desktop and mobile
- Easy-to-use example prompts to get started

**📘 For detailed frontend documentation, screenshots, and customization guide, see [FRONTEND_GUIDE.md](FRONTEND_GUIDE.md)**

### Option 2: Command-Line Interface

Start the traditional CLI chatbot with:
```bash
python chatbot.py
```

### CLI Commands

Once the CLI chatbot is running, you can use these commands:

- Type any question to chat with the bot
- `history` - View the conversation history
- `reset` - Clear the conversation history
- `quit` or `exit` - Exit the chatbot

### Example Interaction

```
You: What is RAG?

🤖 Assistant: RAG stands for Retrieval-Augmented Generation. It's a technique 
that combines large language models with external knowledge retrieval...

You: How does it work?

🤖 Assistant: RAG works through several steps: query processing, retrieval phase,
augmentation, and generation...
```

## 📁 Project Structure

```
Chatbot_agentic_RAG/
├── app.py                  # Web application (Flask) - NEW! 🌐
├── chatbot.py              # CLI application entry point
├── requirements.txt        # Python dependencies
├── .env.example           # Example environment variables
├── .gitignore             # Git ignore file
├── templates/             # HTML templates for web interface
│   └── index.html         # Main chat interface
├── data/
│   └── documents/         # Place your documents here (txt, pdf, md, csv, docx)
├── src/
│   ├── agents/
│   │   └── rag_agent.py   # Agentic RAG implementation
│   ├── tools/
│   │   └── retrieval_tool.py  # Knowledge base search tool
│   └── utils/
│       └── vector_store.py    # Document indexing and retrieval
└── chroma_db/             # Vector database (created automatically)
```

## 📚 Adding Your Own Documents

1. Place your documents in the `data/documents/` directory
2. The chatbot will automatically load and index them on startup
3. The vector store is persisted in `chroma_db/`, so documents are only processed once

**Supported file formats:**
- `.txt` - Plain text files
- `.pdf` - PDF documents
- `.md` - Markdown files
- `.csv` - CSV data files
- `.docx` - Microsoft Word documents

## 🔧 Configuration

You can customize the chatbot by modifying these settings in your `.env` file:

```env
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-3.5-turbo          # Or gpt-4 for better results
EMBEDDING_MODEL=text-embedding-ada-002
```

## 🎯 How It Works

1. **Document Loading**: Documents are loaded from `data/documents/`
2. **Chunking**: Documents are split into smaller chunks for better retrieval
3. **Embedding**: Each chunk is converted to a vector using OpenAI embeddings
4. **Vector Storage**: Embeddings are stored in ChromaDB for fast similarity search
5. **Agent Loop**: When you ask a question:
   - The agent reasons about what information it needs
   - It uses the retrieval tool to search the knowledge base
   - Retrieved context is combined with the query
   - The LLM generates a response based on the context
   - The conversation history is maintained for follow-up questions

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

Built with:
- [LangChain](https://github.com/langchain-ai/langchain) - Framework for LLM applications
- [ChromaDB](https://www.trychroma.com/) - Vector database
- [OpenAI](https://openai.com/) - LLM and embeddings
