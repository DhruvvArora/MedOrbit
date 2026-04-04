import os
from pathlib import Path
from agents.psychologist_knowledge.config import RESOURCE_DIR

def load_documents():
    """
    Scrapes the text and markdown files out of the resources/psychology folder.
    Returns: List of dicts [{"file": "name.md", "text": "..."}]
    """
    docs = []
    if not os.path.exists(RESOURCE_DIR):
        print(f"Warning: Resource directory {RESOURCE_DIR} does not exist.")
        return docs

    valid_extensions = [".txt", ".md"]
    for root, _, files in os.walk(RESOURCE_DIR):
        for file in files:
            path = Path(root) / file
            if path.suffix in valid_extensions:
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        docs.append({
                            "file": str(path.relative_to(RESOURCE_DIR)),
                            "text": f.read()
                        })
                except Exception as e:
                    print(f"Could not read {file}: {e}")
    return docs
