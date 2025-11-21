"""
config.py

Shared configuration for the RAG demo.
Keeps all paths and constants in one place.
"""

from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_SOURCE_DIR = DATA_DIR / "data_sources"
OUTPUT_DIR = DATA_DIR / "outputs"
KNOWLEDGE_LIBRARY_DIR = DATA_DIR / "knowledge_base"
MODEL_DIR = DATA_DIR / "models"
PROMPT_DIR = DATA_DIR / "prompts"

# PDF input and Knowledge Library output
PDF_PATH = DATA_SOURCE_DIR / "book.pdf"
KNOWLEDGE_LIBRARY_PATH = KNOWLEDGE_LIBRARY_DIR / "knowledge_library.json"

# Embedding model (local, free)
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

# RAG settings
TOP_K = 3  # how many knowledge cards to retrieve

# Prompt templates (stored as plain text files)
SYSTEM_PROMPT_PATH = PROMPT_DIR / "system_prompt.txt"
USER_PROMPT_PATH = PROMPT_DIR / "user_prompt.txt"

# Long-term memory log (JSONL: one JSON per line)
CONVERSATION_LOG_PATH = OUTPUT_DIR / "conversation_log.jsonl"


