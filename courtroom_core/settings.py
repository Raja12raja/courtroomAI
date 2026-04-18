"""Paths and constants for RAG assets (project root)."""
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
FAISS_INDEX_PATH = ROOT_DIR / "faiss.index"
TEXTS_PKL_PATH = ROOT_DIR / "texts.pkl"
SENTENCE_TRANSFORMER_MODEL = "all-MiniLM-L6-v2"
LLM_ENDPOINT = "databricks-llama-4-maverick"
