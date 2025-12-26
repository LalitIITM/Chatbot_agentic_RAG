# Document Format Support

This document describes the multiple document format support in the Chatbot Agentic RAG system.

## Supported Formats

The system now supports the following document formats in the `data/documents` directory:

### 1. Text Files (.txt)
Plain text documents with UTF-8 encoding.

**Example files:**
- `ai_basics.txt`
- `python_best_practices.txt`
- `rag_explained.txt`

### 2. Markdown Files (.md)
Markdown-formatted documents with proper heading structure and formatting.

**Example files:**
- `machine_learning_basics.md`

### 3. CSV Files (.csv)
Comma-separated value files containing structured data. Each row becomes a separate document chunk.

**Example files:**
- `learning_topics.csv`

### 4. PDF Files (.pdf)
Portable Document Format files. The system extracts text from each page.

**Usage:** Simply place `.pdf` files in `data/documents/` directory.

### 5. Word Documents (.docx)
Microsoft Word documents in the DOCX format.

**Usage:** Simply place `.docx` files in `data/documents/` directory.

## Implementation Details

The document loading functionality is implemented in `src/utils/vector_store.py` using the following loaders:

- **TextLoader**: For .txt files
- **UnstructuredMarkdownLoader**: For .md files  
- **CSVLoader**: For .csv files
- **PyPDFLoader**: For .pdf files
- **UnstructuredWordDocumentLoader**: For .docx files

## How to Add New Documents

1. Place your document files in `data/documents/` directory
2. Ensure the file has one of the supported extensions (.txt, .md, .csv, .pdf, .docx)
3. Delete the `chroma_db/` directory if you want to force re-indexing
4. Restart the application

The system will automatically:
- Detect all supported file types
- Load and parse the content
- Split content into appropriate chunks
- Create embeddings
- Store in the vector database

## Dependencies

The following Python packages are required for document format support:

```
pypdf>=5.1.0          # PDF support
python-docx>=1.1.2    # Word document support
unstructured>=0.16.9  # Markdown and other format support
markdown>=3.4.0       # Markdown rendering
```

These are included in `requirements.txt` and will be installed automatically.

## Error Handling

The system includes robust error handling:
- If a specific file fails to load, it will be skipped with an error message
- Other documents will continue to load successfully
- The system will create an empty vector store if no documents are found
