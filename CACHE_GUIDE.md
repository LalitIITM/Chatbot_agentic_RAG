# Query Caching Implementation

## Overview

This document describes the query caching implementation that reduces LLM API costs by caching responses to similar queries.

## Database Used

The system uses **ChromaDB** as the vector database:
1. **Document Storage**: For storing and searching document embeddings (in `chroma_db/`)
2. **Query Cache**: For storing and searching cached query-response pairs (in `query_cache_db/`)

Both use ChromaDB with OpenAI embeddings for semantic similarity matching.

## How Query Caching Works

### Architecture

```
User Query → Cache Check → Cache Hit? 
                              ↓ Yes: Return cached response (fast, cheap)
                              ↓ No: Call LLM (slower, expensive)
                                    ↓
                              Store in cache for future queries
```

### Key Features

1. **Semantic Matching**: Uses embeddings to find similar queries, not just exact matches
2. **Configurable Threshold**: Control how similar queries must be to trigger cache hits
3. **TTL (Time-to-Live)**: Cache entries expire after a configurable time
4. **Session Memory Preserved**: Conversation context is maintained even with cached responses
5. **Cost Optimization**: Significantly reduces OpenAI API costs

### Configuration

Set these in your `.env` file:

```env
# Enable/disable caching
QUERY_CACHE_ENABLED=True

# Similarity threshold (0.90-0.99 recommended)
# Higher = more strict, fewer cache hits, more accurate
# Lower = more lenient, more cache hits, more savings
QUERY_CACHE_SIMILARITY_THRESHOLD=0.95

# Time-to-live in seconds (default: 24 hours)
QUERY_CACHE_TTL=86400
```

### Cost Comparison

Example costs per query:
- **LLM call (GPT-3.5)**: ~$0.002 per 1K tokens (varies by conversation)
- **Cache hit**: ~$0.0001 per 1K tokens (just embedding lookup)
- **Savings**: ~95% cost reduction for cached queries

For 100 queries where 50 are similar:
- **Without cache**: 100 LLM calls = ~$0.20
- **With cache**: 50 LLM calls + 50 cache lookups = ~$0.105
- **Savings**: ~$0.095 (47.5%)

## Usage Examples

### Example 1: Basic Usage

```python
from src.utils.query_cache import QueryCache

# Initialize cache
cache = QueryCache(
    enabled=True,
    similarity_threshold=0.95,
    cache_ttl=86400  # 24 hours
)

# Check cache
cached_response = cache.get("What is machine learning?")
if cached_response:
    print("Cache hit!", cached_response)
else:
    # Call LLM, get response
    response = llm.generate("What is machine learning?")
    # Store in cache
    cache.set("What is machine learning?", response)
```

### Example 2: With Agent (Already Integrated)

The cache is already integrated into the chatbot:

```python
# In chatbot.py or app.py, cache is automatically initialized
chatbot = AgenticRAGChatbot()

# First query - calls LLM
response1 = chatbot.chat("What is RAG?")  # Cache miss → LLM call

# Similar query - uses cache
response2 = chatbot.chat("What's RAG?")   # Cache hit → instant response!

# Very different query - calls LLM
response3 = chatbot.chat("What is Python?")  # Cache miss → LLM call
```

## Session Memory Integration

The caching system preserves conversation memory:

1. **Cache Hit**: Cached response is returned AND added to conversation memory
2. **Cache Miss**: Normal flow proceeds, memory is maintained as usual
3. **Follow-up Context**: The agent can still use conversation history for follow-up questions

Example:
```
User: "What is RAG?"
Bot: [Cache hit or miss] "RAG is Retrieval-Augmented Generation..."

User: "How does it work?"  # Follow-up question
Bot: [Uses conversation memory] "RAG works by first retrieving relevant documents..."
```

## Implementation Details

### QueryCache Class

Located in `src/utils/query_cache.py`, provides:

- `get(query, session_id)`: Check cache for similar queries
- `set(query, response, session_id)`: Store query-response pair
- `clear()`: Clear all cache entries
- `get_stats()`: Get cache statistics

### Agent Integration

Modified `src/agents/rag_agent.py`:

1. Added `query_cache` parameter to `__init__`
2. Modified `chat()` method to check cache first
3. Cached responses are added to conversation memory

### Similarity Calculation

Uses ChromaDB's similarity search with L2 distance:
- Distance → Similarity conversion: `similarity = 1 / (1 + distance)`
- Threshold check: `similarity >= threshold`
- TTL check: `current_time - timestamp <= ttl`

## Testing

Run the test suite:
```bash
python test_query_cache.py
```

Run the demo:
```bash
python demo_cache.py
```

## Troubleshooting

### Cache not working?

1. Check `QUERY_CACHE_ENABLED=True` in `.env`
2. Verify OpenAI API key is set
3. Check similarity threshold (try lowering to 0.90 for testing)

### Too many cache misses?

- Lower the similarity threshold (e.g., 0.90 instead of 0.95)
- More lenient matching = more cache hits

### Too many cache hits on unrelated queries?

- Raise the similarity threshold (e.g., 0.98 instead of 0.95)
- Stricter matching = more accurate results

## Best Practices

1. **Threshold Tuning**: Start with 0.95, adjust based on your needs
2. **TTL Setting**: 
   - Stable knowledge: 24-48 hours
   - Frequently changing: 1-6 hours
3. **Monitoring**: Check cache stats periodically: `cache.get_stats()`
4. **Cost Analysis**: Track API usage to measure savings

## Future Enhancements

Possible improvements:
- [ ] Per-user cache (currently session-based)
- [ ] Cache warm-up from common queries
- [ ] Analytics dashboard for cache performance
- [ ] Automatic threshold tuning based on feedback
- [ ] Cache invalidation by topic/document
