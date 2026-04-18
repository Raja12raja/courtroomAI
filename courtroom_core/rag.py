"""FAISS + sentence-transformer retrieval over legal text chunks."""
import pickle

import faiss
from sentence_transformers import SentenceTransformer

from courtroom_core.settings import (
    FAISS_INDEX_PATH,
    SENTENCE_TRANSFORMER_MODEL,
    TEXTS_PKL_PATH,
)

model = SentenceTransformer(SENTENCE_TRANSFORMER_MODEL)

with TEXTS_PKL_PATH.open("rb") as f:
    texts = pickle.load(f)

index = faiss.read_index(str(FAISS_INDEX_PATH))


def search(query: str, top_k: int = 3) -> str:
    """Retrieve top-k relevant legal context chunks for a given query."""
    q = model.encode([query])
    D, I = index.search(q, top_k)
    chunks = [texts[i][:600] for i in I[0] if i < len(texts)]
    return "\n\n---\n\n".join(chunks)

