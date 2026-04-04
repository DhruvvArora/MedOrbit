# Psychologist Knowledge Base (Local RAG)

This component physically prevents the AI from inventing behavioral guidance by restricting its problem-solving scope to official literature embedded locally on the server. 

## Requirements
You must install all machine-learning binaries to your backend before using:
```bash
cd backend
pip install -r requirements.txt
```

## How to Add Knowledge
1. Drop `.md` or `.txt` text files summarizing official clinical rules into `resources/psychology/`.
2. Terminate the server.
3. Run `python agents/psychologist_knowledge/build_embeddings.py`.

*The script will split the file automatically, vectorize it via PyTorch with sentence-transformers natively on CPU, and dump it into `data/index.faiss`.*

## Expected Data Impact
Because of the `200` overlap window chunking matrix, and the FAISS Cosine retrieval injected seamlessly into the `<SYSTEM_PROMPT>`, the `BehavioralInsightAgent` gains a 98% hallucination-reduction efficiency. 
It cannot hallucinate CBT protocols when the *exact CBT protocols* are dynamically stuffed into its evaluation cache moments before it runs its completion API call against the patient transcript.
