"""
Vector Store Manager
Handles document loading, embedding, and vector storage using ChromaDB
"""

import os
from typing import List, Optional
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document


class VectorStoreManager:
    """Manages document ingestion and vector storage"""
    
    def __init__(
        self,
        documents_dir: str = "data/documents",
        persist_directory: str = "chroma_db",
        embedding_model: str = "text-embedding-ada-002",
        chunk_size: int = 1000,
        chunk_overlap: int = 200
    ):
        """
        Initialize the vector store manager
        
        Args:
            documents_dir: Directory containing documents to load
            persist_directory: Directory to persist the vector store
            embedding_model: OpenAI embedding model to use
            chunk_size: Size of text chunks for splitting
            chunk_overlap: Overlap between chunks
        """
        self.documents_dir = documents_dir
        self.persist_directory = persist_directory
        self.embeddings = OpenAIEmbeddings(model=embedding_model)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
        )
        self.vectorstore: Optional[Chroma] = None
    
    def load_documents(self) -> List[Document]:
        """Load documents from the documents directory"""
        if not os.path.exists(self.documents_dir):
            os.makedirs(self.documents_dir)
            print(f"Created documents directory: {self.documents_dir}")
            return []
        
        loader = DirectoryLoader(
            self.documents_dir,
            glob="**/*.txt",
            loader_cls=TextLoader,
            show_progress=True
        )
        
        try:
            documents = loader.load()
            print(f"Loaded {len(documents)} documents")
            return documents
        except Exception as e:
            print(f"Error loading documents: {e}")
            return []
    
    def split_documents(self, documents: List[Document]) -> List[Document]:
        """Split documents into chunks"""
        chunks = self.text_splitter.split_documents(documents)
        print(f"Split into {len(chunks)} chunks")
        return chunks
    
    def create_vectorstore(self, documents: List[Document]) -> Chroma:
        """Create or load vector store from documents"""
        if os.path.exists(self.persist_directory):
            print(f"Loading existing vector store from {self.persist_directory}")
            self.vectorstore = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings
            )
        else:
            print(f"Creating new vector store at {self.persist_directory}")
            chunks = self.split_documents(documents)
            
            if not chunks:
                print("No documents to index. Creating empty vector store.")
                # Create with a dummy document
                chunks = [Document(page_content="Empty knowledge base", metadata={})]
            
            self.vectorstore = Chroma.from_documents(
                documents=chunks,
                embedding=self.embeddings,
                persist_directory=self.persist_directory
            )
        
        return self.vectorstore
    
    def get_retriever(self, search_kwargs: dict = None):
        """Get a retriever from the vector store"""
        if self.vectorstore is None:
            raise ValueError("Vector store not initialized. Call create_vectorstore first.")
        
        if search_kwargs is None:
            search_kwargs = {"k": 4}
        
        return self.vectorstore.as_retriever(search_kwargs=search_kwargs)
    
    def add_documents(self, documents: List[Document]):
        """Add new documents to existing vector store"""
        if self.vectorstore is None:
            raise ValueError("Vector store not initialized.")
        
        chunks = self.split_documents(documents)
        self.vectorstore.add_documents(chunks)
        print(f"Added {len(chunks)} new chunks to vector store")
    
    def similarity_search(self, query: str, k: int = 4) -> List[Document]:
        """Perform similarity search"""
        if self.vectorstore is None:
            raise ValueError("Vector store not initialized.")
        
        return self.vectorstore.similarity_search(query, k=k)
