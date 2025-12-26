# Usage Guide - Agentic RAG Chatbot

## Quick Start

### 1. Setup Environment

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure API key
cp .env.example .env
# Edit .env and add your OpenAI API key
```

### 2. Run the Chatbot

```bash
python chatbot.py
```

## Example Conversations

### Basic Questions

```
You: What is artificial intelligence?

🤖 Assistant: [Uses knowledge_base_search to find information about AI]
Artificial Intelligence is the simulation of human intelligence 
processes by machines, especially computer systems...
```

### Follow-up Questions (Using Memory)

```
You: What is RAG?

🤖 Assistant: RAG stands for Retrieval-Augmented Generation...

You: How does it work?

🤖 Assistant: [Maintains context from previous question]
RAG works through several steps: query processing, retrieval phase,
augmentation, and generation...
```

### Complex Queries (Agent Reasoning)

```
You: Compare traditional AI with agentic RAG systems

🤖 Assistant: [Agent reasons it needs multiple pieces of information]
[Uses knowledge_base_search multiple times]
[Synthesizes information to provide comprehensive answer]
```

## CLI Commands

While chatting with the bot:

- **Type any question**: Chat normally with the bot
- **`history`**: View conversation history
- **`reset`**: Clear conversation history and start fresh
- **`quit` or `exit`**: Exit the chatbot

## Adding Custom Documents

1. Create text files (.txt) with your content
2. Place them in `data/documents/` directory
3. Delete the `chroma_db/` folder (if it exists)
4. Restart the chatbot to re-index documents

### Document Format

Documents should be plain text files. The system will:
- Automatically chunk long documents
- Generate embeddings for each chunk
- Store them for semantic search

Example document structure:
```
Title of Document

Section 1: Introduction
Content for section 1...

Section 2: Details
Content for section 2...
```

## Advanced Configuration

### Model Selection

Edit `.env` to use different models:

```env
# Use GPT-4 for better reasoning (higher cost)
OPENAI_MODEL=gpt-4

# Or use GPT-3.5-turbo for faster responses (lower cost)
OPENAI_MODEL=gpt-3.5-turbo
```

### Retrieval Parameters

Edit `chatbot.py` to customize retrieval:

```python
retriever = self.vector_store_manager.get_retriever(
    search_kwargs={"k": 4}  # Number of documents to retrieve
)
```

### Chunk Size

Edit `src/utils/vector_store.py`:

```python
self.text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,      # Size of each chunk
    chunk_overlap=200,    # Overlap between chunks
    length_function=len,
)
```

## Troubleshooting

### "OPENAI_API_KEY not found"
- Make sure you created `.env` file (not just `.env.example`)
- Verify your API key is correct in `.env`

### "No module named 'langchain'"
- Install dependencies: `pip install -r requirements.txt`
- Make sure virtual environment is activated

### "No relevant information found"
- Check that documents are in `data/documents/`
- Verify documents are `.txt` format
- Try rephrasing your question

### Slow responses
- Use GPT-3.5-turbo instead of GPT-4
- Reduce the number of retrieved documents (k parameter)
- Check your internet connection

## Performance Tips

1. **Start with few documents**: Test with 2-3 documents initially
2. **Use GPT-3.5-turbo**: Faster and cheaper for development
3. **Monitor token usage**: Check OpenAI dashboard for usage
4. **Reuse vector store**: The `chroma_db/` folder is cached

## Understanding Agent Behavior

The agent uses reasoning to decide:
- When to search the knowledge base
- What search queries to use
- How to combine multiple pieces of information
- When it has enough information to answer

You'll see the agent's reasoning in verbose mode (enabled by default).

## Best Practices

1. **Document Organization**: Group related documents in subdirectories
2. **Document Quality**: Use well-structured, clear documents
3. **API Keys**: Never commit `.env` file to version control
4. **Testing**: Test with known questions before deployment
5. **Monitoring**: Keep track of API costs on OpenAI dashboard
