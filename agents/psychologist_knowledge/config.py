import os
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
RESOURCE_DIR = BASE_DIR / "resources" / "psychology"
DATA_DIR = BASE_DIR / "agents" / "psychologist_knowledge" / "data"

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

INDEX_PATH = DATA_DIR / "index.faiss"
CHUNKS_PATH = DATA_DIR / "chunks.jsonl"
METADATA_PATH = DATA_DIR / "metadata.json"

# Embedding Model Constraints
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
CHUNK_SIZE_WORDS = 500
CHUNK_OVERLAP_WORDS = 100
