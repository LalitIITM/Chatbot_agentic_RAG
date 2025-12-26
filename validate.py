"""
Simple validation script for the Agentic RAG Chatbot
Validates file structure and syntax without requiring dependencies
"""

import os
import ast
import sys

def validate_python_syntax(filepath):
    """Check if a Python file has valid syntax"""
    try:
        with open(filepath, 'r') as f:
            code = f.read()
        ast.parse(code)
        return True, "Valid syntax"
    except SyntaxError as e:
        return False, f"Syntax error: {e}"
    except Exception as e:
        return False, f"Error: {e}"

def check_file_exists(filepath):
    """Check if a file exists"""
    return os.path.exists(filepath)

def main():
    print("="*60)
    print("Agentic RAG Chatbot - Validation")
    print("="*60)
    
    # Check file structure
    print("\n1. Checking file structure...")
    required_files = {
        "Main Files": [
            "chatbot.py",
            "requirements.txt",
            ".env.example",
            ".gitignore",
            "README.md"
        ],
        "Source Code": [
            "src/__init__.py",
            "src/agents/__init__.py",
            "src/agents/rag_agent.py",
            "src/tools/__init__.py",
            "src/tools/retrieval_tool.py",
            "src/utils/__init__.py",
            "src/utils/vector_store.py"
        ],
        "Sample Documents": [
            "data/documents/ai_basics.txt",
            "data/documents/rag_explained.txt",
            "data/documents/python_best_practices.txt"
        ]
    }
    
    all_files_present = True
    for category, files in required_files.items():
        print(f"\n  {category}:")
        for filepath in files:
            exists = check_file_exists(filepath)
            status = "✓" if exists else "✗"
            print(f"    {status} {filepath}")
            if not exists:
                all_files_present = False
    
    if all_files_present:
        print("\n  ✓ All required files present")
    else:
        print("\n  ✗ Some files are missing")
        return 1
    
    # Check Python syntax
    print("\n2. Checking Python syntax...")
    python_files = [
        "chatbot.py",
        "src/__init__.py",
        "src/agents/__init__.py",
        "src/agents/rag_agent.py",
        "src/tools/__init__.py",
        "src/tools/retrieval_tool.py",
        "src/utils/__init__.py",
        "src/utils/vector_store.py"
    ]
    
    all_syntax_valid = True
    for filepath in python_files:
        valid, message = validate_python_syntax(filepath)
        status = "✓" if valid else "✗"
        print(f"  {status} {filepath}: {message}")
        if not valid:
            all_syntax_valid = False
    
    if all_syntax_valid:
        print("\n  ✓ All Python files have valid syntax")
    else:
        print("\n  ✗ Some Python files have syntax errors")
        return 1
    
    # Check content of key files
    print("\n3. Checking key components...")
    
    # Check requirements.txt
    with open("requirements.txt", 'r') as f:
        requirements = f.read()
    required_packages = ["langchain", "chromadb", "openai", "tiktoken", "python-dotenv"]
    for package in required_packages:
        if package in requirements:
            print(f"  ✓ {package} in requirements.txt")
        else:
            print(f"  ✗ {package} missing from requirements.txt")
            all_syntax_valid = False
    
    # Check .env.example
    with open(".env.example", 'r') as f:
        env_content = f.read()
    if "OPENAI_API_KEY" in env_content:
        print(f"  ✓ OPENAI_API_KEY in .env.example")
    else:
        print(f"  ✗ OPENAI_API_KEY missing from .env.example")
    
    # Final summary
    print("\n" + "="*60)
    print("Validation Summary")
    print("="*60)
    
    if all_files_present and all_syntax_valid:
        print("\n✓ All validations passed!")
        print("\n📋 Next steps to use the chatbot:")
        print("  1. Install dependencies:")
        print("     pip install -r requirements.txt")
        print("\n  2. Configure API key:")
        print("     cp .env.example .env")
        print("     # Edit .env and add your OPENAI_API_KEY")
        print("\n  3. Run the chatbot:")
        print("     python chatbot.py")
        print("\n  4. Add your own documents:")
        print("     Place .txt files in data/documents/")
        return 0
    else:
        print("\n✗ Some validations failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
