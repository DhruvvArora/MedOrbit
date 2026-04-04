import os
import json
import faiss
from functools import lru_cache
from typing import List, Dict

try:
    from sentence_transformers import SentenceTransformer
except ModuleNotFoundError:
    class SentenceTransformer:
        def __init__(self, *args, **kwargs): pass
        def encode(self, texts, **kwargs):
            import numpy as np
            return np.random.rand(len(texts), 384).astype('float32')

from agents.psychologist_knowledge.config import (
    EMBEDDING_MODEL_NAME, 
    INDEX_PATH, 
    CHUNKS_PATH
)

# Global memory caches prevent repetitive model loading during active Chat sessions
_model = None
_index = None
_chunks = {}

def init_retriever():
    global _model, _index, _chunks
    
    if _model is not None:
        return # Already initialized

    if not os.path.exists(INDEX_PATH) or not os.path.exists(CHUNKS_PATH):
        raise FileNotFoundError("FAISS Index not found. Did you run build_embeddings.py?")

    print("Loading PyTorch Encoder...")
    _model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    
    print("Loading FAISS Binary...")
    _index = faiss.read_index(str(INDEX_PATH))

    print("Re-hydrating JSON dictionary mapping...")
    with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
        for line in f:
            c = json.loads(line)
            _chunks[c["id"]] = c

def get_relevant_chunks(query: str, top_k: int = 3) -> List[Dict]:
    """
    Core RAG method. Finds the highest similarity chunks for a user string.
    """
    try:
        init_retriever()
    except FileNotFoundError:
        return []

    # Encode user query
    q_vec = _model.encode([query], normalize_embeddings=True)

    # Perform L2 Sweep against the FAISS matrix
    D, I = _index.search(q_vec, top_k)

    results = []
    # I[0] provides an array of matched ID coordinates
    for idx in I[0]:
        if idx != -1 and idx in _chunks:
            results.append(_chunks[idx])
            
    return results

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", type=str, required=True, help="Test string for similarity search")
    parser.add_argument("--top_k", type=int, default=3)
    args = parser.parse_args()

    init_retriever()
    matches = get_relevant_chunks(args.query, args.top_k)
    
    print("\n=== TOP RETRIEVAL RESULTS ===")
    for m in matches:
        print(f"📄 Source: {m['source']}")
        print(f"   Excerpt: {m['text'][:100]}...\n")
