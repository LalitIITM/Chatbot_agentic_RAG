"""
Vector Store Manager
Handles document loading, embedding, and vector storage using ChromaDB
"""

import os
from typing import List, Optional
from langchain_community.document_loaders import (
    DirectoryLoader, 
    TextLoader,
    PyPDFLoader,
    UnstructuredMarkdownLoader,
    CSVLoader,
    UnstructuredWordDocumentLoader
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document


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
        """Load documents from the documents directory
        
        Supports multiple file formats:
        - .txt (Text files)
        - .pdf (PDF documents)
        - .md (Markdown files)
        - .csv (CSV files)
        - .docx (Word documents)
        """
        if not os.path.exists(self.documents_dir):
            os.makedirs(self.documents_dir)
            print(f"Created documents directory: {self.documents_dir}")
            return []
        
        all_documents = []
        
        # Define loaders for different file types
        loaders_config = [
            {"glob": "**/*.txt", "loader_cls": TextLoader},
            {"glob": "**/*.md", "loader_cls": UnstructuredMarkdownLoader},
            {"glob": "**/*.csv", "loader_cls": CSVLoader},
        ]
        
        # Load documents for each file type
        for config in loaders_config:
            try:
                loader = DirectoryLoader(
                    self.documents_dir,
                    glob=config["glob"],
                    loader_cls=config["loader_cls"],
                    show_progress=False,
                    silent_errors=True
                )
                documents = loader.load()
                if documents:
                    print(f"Loaded {len(documents)} {config['glob']} files")
                    all_documents.extend(documents)
            except Exception as e:
                print(f"Error loading {config['glob']} files: {e}")
        
        # Load PDF files separately (require different handling)
        try:
            pdf_files = [f for f in os.listdir(self.documents_dir) if f.endswith('.pdf')]
            for pdf_file in pdf_files:
                try:
                    pdf_path = os.path.join(self.documents_dir, pdf_file)
                    loader = PyPDFLoader(pdf_path)
                    documents = loader.load()
                    all_documents.extend(documents)
                    print(f"Loaded PDF: {pdf_file}")
                except Exception as e:
                    print(f"Error loading PDF {pdf_file}: {e}")
        except Exception as e:
            print(f"Error processing PDF files: {e}")
        
        # Load DOCX files separately
        try:
            docx_files = [f for f in os.listdir(self.documents_dir) if f.endswith('.docx')]
            for docx_file in docx_files:
                try:
                    docx_path = os.path.join(self.documents_dir, docx_file)
                    loader = UnstructuredWordDocumentLoader(docx_path)
                    documents = loader.load()
                    all_documents.extend(documents)
                    print(f"Loaded DOCX: {docx_file}")
                except Exception as e:
                    print(f"Error loading DOCX {docx_file}: {e}")
        except Exception as e:
            print(f"Error processing DOCX files: {e}")
        
        print(f"Total documents loaded: {len(all_documents)}")
        return all_documents
    
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
