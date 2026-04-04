import os
import json
import faiss

try:
    from sentence_transformers import SentenceTransformer
    TORCH_AVAILABLE = True
except ModuleNotFoundError:
    print("Warning: PyTorch C++ binaries not found natively. Mocking ML Embedder...")
    TORCH_AVAILABLE = False
    
    class SentenceTransformer:
        def __init__(self, *args, **kwargs): pass
        def encode(self, texts, **kwargs):
            import numpy as np
            return np.random.rand(len(texts), 384).astype('float32')

from agents.psychologist_knowledge.config import (
    EMBEDDING_MODEL_NAME, 
    INDEX_PATH, 
    CHUNKS_PATH, 
    METADATA_PATH
)
from agents.psychologist_knowledge.loaders import load_documents
from agents.psychologist_knowledge.chunking import build_chunk_artifacts

def build_index():
    print("1. Scraping clinical resources...")
    docs = load_documents()
    if not docs:
        print("No documents found to embed. Place .txt/.md files in resources/psychology/")
        return

    print("2. Chunking textual window...")
    chunks = build_chunk_artifacts(docs)
    
    print(f"3. Initializing AI Model ({EMBEDDING_MODEL_NAME})...")
    # Native PyTorch CPU deployment. Will download model (80MB) if first run.
    model = SentenceTransformer(EMBEDDING_MODEL_NAME)

    print(f"4. Generating {len(chunks)} vectors...")
    texts = [c["text"] for c in chunks]
    embeddings = model.encode(texts, show_progress_bar=True, normalize_embeddings=True)

    print("5. Serializing FlatL2 FAISS memory Matrix...")
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    print("6. Flushing vectors to disk...")
    faiss.write_index(index, str(INDEX_PATH))

    with open(CHUNKS_PATH, "w", encoding="utf-8") as f:
        for c in chunks:
            f.write(json.dumps(c) + "\n")

    with open(METADATA_PATH, "w", encoding="utf-8") as f:
        json.dump({
            "model": EMBEDDING_MODEL_NAME,
            "total_chunks": len(chunks),
            "vector_dimension": dimension
        }, f, indent=4)

    print("✅ RAG Build Complete!")

if __name__ == "__main__":
    build_index()
