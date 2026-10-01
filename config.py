"""Central configuration for the arXiv RAG assistant."""
import os
from pathlib import Path

# --- Paths ---
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
CHROMA_DIR = DATA_DIR / "chroma_db"
DATA_DIR.mkdir(exist_ok=True)

# --- Collection ---
COLLECTION_NAME = "arxiv_papers"

# --- Embedding model (runs locally via sentence-transformers) ---
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# --- Chunking ---
CHUNK_SIZE_CHARS = 1000
CHUNK_OVERLAP_CHARS = 150

# --- Retrieval ---
TOP_K = 5

# --- Generation (Groq, OpenAI-style chat API, free tier available) ---
# Get a key at https://console.groq.com  then set GROQ_API_KEY in your terminal.
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
LLM_MODEL = os.environ.get("GROQ_MODEL", "openai/gpt-oss-120b")
MAX_TOKENS = 2500
