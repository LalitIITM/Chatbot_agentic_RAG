"""
Retrieval Tool
Tool for retrieving relevant information from the knowledge base
"""

from typing import Optional
from langchain.tools import Tool
from langchain.callbacks.manager import CallbackManagerForToolRun


class RetrievalTool:
    """Tool for retrieving information from the vector store"""
    
    def __init__(self, retriever, name: str = "knowledge_base_search"):
        """
        Initialize the retrieval tool
        
        Args:
            retriever: LangChain retriever object
            name: Name of the tool
        """
        self.retriever = retriever
        self.name = name
    
    def _search(self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None) -> str:
        """
        Search the knowledge base for relevant information
        
        Args:
            query: The search query
            run_manager: Callback manager
            
        Returns:
            Formatted string with retrieved documents
        """
        try:
            docs = self.retriever.get_relevant_documents(query)
            
            if not docs:
                return "No relevant information found in the knowledge base."
            
            # Format the results
            result = "Retrieved Information:\n\n"
            for i, doc in enumerate(docs, 1):
                result += f"[Document {i}]\n"
                result += f"{doc.page_content}\n"
                if doc.metadata:
                    result += f"Source: {doc.metadata.get('source', 'Unknown')}\n"
                result += "\n"
            
            return result.strip()
        except Exception as e:
            return f"Error retrieving information: {str(e)}"
    
    def as_tool(self) -> Tool:
        """Convert to LangChain Tool"""
        return Tool(
            name=self.name,
            func=self._search,
            description=(
                "Search the knowledge base for relevant information. "
                "Use this tool when you need to find specific information "
                "from documents to answer user questions. "
                "Input should be a search query string."
            )
        )
