from typing import List, Dict
from agents.psychologist_knowledge.config import CHUNK_SIZE_WORDS, CHUNK_OVERLAP_WORDS

def chunk_text(text: str, chunk_size: int = CHUNK_SIZE_WORDS, overlap: int = CHUNK_OVERLAP_WORDS) -> List[str]:
    """
    Splits text cleanly using a sliding word window.
    """
    words = text.split()
    chunks = []
    
    if not words:
        return chunks
        
    step_size = chunk_size - overlap
    # Ensure step_size is at least 1 to prevent infinite loops
    step_size = max(1, step_size)
    
    for i in range(0, len(words), step_size):
        chunk_words = words[i:i + chunk_size]
        chunks.append(" ".join(chunk_words))
        
        # If we reached the end of the content, stop sliding
        if i + chunk_size >= len(words):
            break
            
    return chunks

def build_chunk_artifacts(documents: List[Dict]) -> List[Dict]:
    """
    Transforms raw files into atomic JSON chunks with structural metadata.
    """
    all_chunks = []
    global_id = 0
    
    for doc in documents:
        raw_chunks = chunk_text(doc["text"])
        for idx, text in enumerate(raw_chunks):
            # Skip empty or trivially small garbage chunks
            if len(text.strip()) < 10:
                continue
                
            all_chunks.append({
                "id": global_id,
                "source": doc["file"],
                "text": text
            })
            global_id += 1
            
    return all_chunks
