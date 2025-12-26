"""
Agentic RAG Agent
An agent that uses reasoning and tools to answer questions using RAG
"""

from typing import List, Optional
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain.tools import Tool
from src.utils.query_cache import QueryCache


class AgenticRAGAgent:
    """An agentic RAG system with reasoning capabilities"""
    
    def __init__(
        self,
        tools: List[Tool],
        model_name: str = "gpt-3.5-turbo",
        temperature: float = 0.7,
        max_iterations: int = 10,
        verbose: bool = True,
        query_cache: Optional[QueryCache] = None,
        session_id: str = "default"
    ):
        """
        Initialize the agentic RAG agent
        
        Args:
            tools: List of tools available to the agent
            model_name: OpenAI model to use
            temperature: Temperature for generation
            max_iterations: Maximum reasoning iterations
            verbose: Whether to print agent reasoning
            query_cache: Optional query cache for reducing LLM calls
            session_id: Session identifier for cache and memory management
        """
        self.tools = tools
        self.model_name = model_name
        self.temperature = temperature
        self.max_iterations = max_iterations
        self.verbose = verbose
        self.query_cache = query_cache
        self.session_id = session_id
        
        # Initialize LLM
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=temperature
        )
        
        # Initialize memory
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        # Create the agent
        self.agent_executor = self._create_agent()
    
    def _create_agent(self) -> AgentExecutor:
        """Create the agent with tools and reasoning capabilities"""
        
        # Define the system prompt for the agent
        system_prompt = """You are a helpful AI assistant with access to a knowledge base.

You can use the available tools to search for information and answer user questions accurately.

When answering questions:
1. Think step-by-step about what information you need
2. Use the knowledge_base_search tool to find relevant information
3. Synthesize the retrieved information to provide clear, accurate answers
4. If you cannot find relevant information, say so honestly
5. Maintain context from the conversation history

Always be helpful, accurate, and concise in your responses."""

        # Create the prompt template
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="chat_history", optional=True),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        # Create the agent
        agent = create_openai_functions_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=prompt
        )
        
        # Create the agent executor
        agent_executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            memory=self.memory,
            verbose=self.verbose,
            max_iterations=self.max_iterations,
            handle_parsing_errors=True
        )
        
        return agent_executor
    
    def chat(self, message: str) -> str:
        """
        Process a user message and return a response
        
        Args:
            message: User's message
            
        Returns:
            Agent's response
        """
        try:
            # Check cache first if enabled
            if self.query_cache:
                cached_response = self.query_cache.get(message, self.session_id)
                if cached_response:
                    # Add to memory for context continuity
                    self.memory.chat_memory.add_user_message(message)
                    self.memory.chat_memory.add_ai_message(cached_response)
                    return cached_response
            
            # Cache miss or caching disabled - invoke agent
            response = self.agent_executor.invoke({"input": message})
            response_text = response.get("output", "I apologize, but I couldn't generate a response.")
            
            # Store in cache if enabled
            if self.query_cache:
                self.query_cache.set(message, response_text, self.session_id)
            
            return response_text
        except Exception as e:
            error_type = type(e).__name__
            return f"Error processing message ({error_type}): {str(e)}"
    
    def reset_memory(self):
        """Clear the conversation history"""
        self.memory.clear()
    
    def get_conversation_history(self) -> str:
        """Get the conversation history as a string"""
        try:
            messages = self.memory.chat_memory.messages
            history = []
            for msg in messages:
                role = "User" if msg.type == "human" else "Assistant"
                history.append(f"{role}: {msg.content}")
            return "\n".join(history)
        except Exception:
            return "No conversation history available."
