# Architecture and Design

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    User Interface (CLI/Web)                  │
│                 (chatbot.py / app.py)                        │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                   Agentic RAG Agent                          │
│            (src/agents/rag_agent.py)                         │
│  ┌────────────┐  ┌──────────────┐  ┌──────────────────┐   │
│  │   Memory   │  │ Query Cache  │  │   Agent Loop     │   │
│  │  (History) │  │  (Cost Opt.) │  │   (Reasoning)    │   │
│  └────────────┘  └──────┬───────┘  └──────────────────┘   │
└─────────────────────────┼────────────────┬─────────────────┘
                          │                │
                    Cache Hit?             │ Cache Miss
                          │                │
                          └────────────────▼
                          ┌─────────────────────────────────────┐
                          │          LLM (GPT)                  │
                          └─────────────────────────────────────┘
                                         │
                                         ▼
                          ┌─────────────────────────────────────┐
                          │         Tool Layer                  │
                          │   (src/tools/retrieval_tool.py)     │
                          └────────────┬────────────────────────┘
                                       │
                                       ▼
                          ┌─────────────────────────────────────┐
                          │      Vector Store Manager           │
                          │   (src/utils/vector_store.py)       │
                          │  ┌──────────┐  ┌─────────────────┐ │
                          │  │ ChromaDB │  │   Embeddings    │ │
                          │  │(VectorDB)│  │    (OpenAI)     │ │
                          │  └──────────┘  └─────────────────┘ │
                          └─────────────────────────────────────┘
```

## Component Details

### 1. Query Cache (`src/utils/query_cache.py`) **NEW**

**Responsibilities:**
- Cache query-response pairs for cost optimization
- Perform semantic similarity matching for queries
- Manage cache expiration and TTL
- Provide cache statistics

**Key Features:**
- ChromaDB-based persistent cache storage
- Semantic similarity matching (not just exact matches)
- Configurable similarity threshold
- Time-to-live (TTL) for cache entries
- Session-aware caching

**Cost Savings:**
- Reduces LLM API calls for similar queries
- Only embedding cost for cache lookups (much cheaper than LLM calls)
- Example: GPT-3.5 call ~$0.002/1K tokens vs embedding ~$0.0001/1K tokens

### 2. Vector Store Manager (`src/utils/vector_store.py`)

**Responsibilities:**
- Load documents from filesystem
- Split documents into manageable chunks
- Generate embeddings using OpenAI
- Store vectors in ChromaDB
- Provide retrieval interface

**Key Features:**
- Persistent storage (survives restarts)
- Configurable chunk size and overlap
- Semantic search capabilities

### 3. Retrieval Tool (`src/tools/retrieval_tool.py`)

**Responsibilities:**
- Expose retrieval as a tool for the agent
- Format search queries
- Return formatted results

**Key Features:**
- LangChain Tool integration
- Clear tool description for agent reasoning
- Error handling

### 4. Agentic RAG Agent (`src/agents/rag_agent.py`)

**Responsibilities:**
- Coordinate between tools and LLM
- Maintain conversation history
- Make decisions about when to use tools
- Generate final responses

**Key Features:**
- OpenAI Functions Agent (uses function calling)
- Conversation memory
- Query cache integration
- Multi-step reasoning
- Error recovery

### 5. Main Application (`chatbot.py` / `app.py`)

**Responsibilities:**
- Initialize all components
- Provide CLI interface
- Handle user interaction
- Manage application lifecycle

## Data Flow

### Question Answering Flow (with Query Cache)

1. **User Input**: User types a question
2. **Cache Check**: Agent checks query cache for similar queries
   - **Cache Hit**: Return cached response immediately (add to memory for context)
   - **Cache Miss**: Continue to step 3
3. **Agent Processing**: Agent receives the question and processes it
4. **Reasoning**: Agent decides if it needs to search the knowledge base
5. **Tool Use**: If needed, agent calls `knowledge_base_search` tool
6. **Retrieval**: Tool queries vector store for relevant documents
7. **Context Building**: Retrieved documents are added to context
8. **Generation**: LLM generates response using retrieved context
9. **Cache Storage**: Store query-response pair in cache for future use
10. **Response**: Answer is returned to user
7. **Generation**: LLM generates response using retrieved context
8. **Response**: Answer is returned to user

### Query Cache Flow

1. **Query Embedding**: User query is embedded using OpenAI embeddings
2. **Similarity Search**: Search cached queries using semantic similarity
3. **Threshold Check**: Compare similarity score against threshold
4. **TTL Check**: Verify cached entry hasn't expired
5. **Return**: If valid match found, return cached response; otherwise return None

### Document Indexing Flow

1. **Load**: Read text files from `data/documents/`
2. **Split**: Break documents into chunks
3. **Embed**: Generate vector embeddings for each chunk
4. **Store**: Save embeddings in ChromaDB
5. **Persist**: Write to disk for future use

## Key Design Decisions

### Why LangChain?

- **Abstraction**: High-level abstractions for common patterns
- **Tool Integration**: Easy tool creation and agent integration
- **Memory Management**: Built-in conversation memory
- **Extensibility**: Easy to add new tools and capabilities

### Why ChromaDB?

- **Lightweight**: No external services needed
- **Persistent**: Data stored on disk
- **Fast**: Efficient vector similarity search
- **Simple**: Easy to set up and use

### Why OpenAI Functions Agent?

- **Structured Tool Use**: Function calling is more reliable
- **Better Reasoning**: Explicit tool descriptions help decision-making
- **Error Handling**: Built-in parsing error recovery

## Agentic Behavior

The agent exhibits "agentic" behavior through:

1. **Autonomous Decision Making**: Decides when to search
2. **Multi-step Planning**: Can chain multiple tool calls
3. **Self-reflection**: Can evaluate if retrieved info is sufficient
4. **Context Awareness**: Uses conversation history for follow-ups

## Extension Points

### Adding New Tools

```python
from langchain.tools import Tool

def my_custom_tool(query: str) -> str:
    # Your tool logic here
    return result

custom_tool = Tool(
    name="tool_name",
    func=my_custom_tool,
    description="Description for the agent"
)

# Add to agent
agent = AgenticRAGAgent(tools=[retrieval_tool, custom_tool])
```

### Custom Embeddings

```python
# In vector_store.py
from langchain.embeddings import HuggingFaceEmbeddings

self.embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
```

### Different LLM

```python
# In rag_agent.py
from langchain.llms import Anthropic

self.llm = Anthropic(model="claude-2")
```

## Performance Considerations

### Memory Usage
- ChromaDB keeps index in memory
- Each document chunk uses ~1KB of storage
- 1000 chunks ≈ 1MB memory

### API Costs
- Embeddings: ~$0.0001 per 1K tokens
- GPT-3.5: ~$0.002 per 1K tokens
- GPT-4: ~$0.03 per 1K tokens

### Latency
- Embedding generation: ~100-200ms
- Vector search: <50ms
- LLM generation: 1-5 seconds

## Security Considerations

1. **API Keys**: Stored in `.env`, never committed
2. **Input Validation**: Agent handles malformed queries
3. **Error Messages**: No sensitive information in errors
4. **Rate Limiting**: OpenAI handles rate limits automatically

## Testing Strategy

1. **Unit Tests**: Test individual components
2. **Integration Tests**: Test component interactions
3. **End-to-End Tests**: Test full conversation flows
4. **Manual Testing**: Validate agent behavior

## Future Enhancements

Possible extensions:
- [ ] Web interface (Gradio/Streamlit)
- [ ] Multiple document formats (PDF, DOCX)
- [ ] Advanced retrieval (hybrid search, reranking)
- [ ] Multi-agent collaboration
- [ ] Streaming responses
- [ ] Usage analytics and logging
- [ ] Fine-tuning on specific domains
- [ ] Custom prompt templates
