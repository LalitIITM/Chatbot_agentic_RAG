# Version Compatibility Note

## langchain-text-splitters Version Change

**Previous**: `langchain-text-splitters>=1.0.0`  
**Current**: `langchain-text-splitters>=0.3.0,<1.0.0`

### Reason for Change

This change was necessary to resolve a dependency conflict with `langchain>=0.3.0`. The LangChain 0.3.x series requires `langchain-text-splitters<1.0.0`.

### Impact

- **New installations**: No impact, will install compatible versions
- **Existing installations**: May need to downgrade `langchain-text-splitters` if 1.x was installed
- **Functionality**: No change - the 0.3.x and 1.x versions have compatible APIs for our use case

### Resolution for Existing Installations

If you encounter version conflicts:

```bash
pip uninstall langchain-text-splitters
pip install -r requirements.txt
```

Or use a fresh virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

This aligns with the official LangChain package compatibility matrix.
