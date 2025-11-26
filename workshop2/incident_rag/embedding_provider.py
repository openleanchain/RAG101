# workshop2/incident_rag/embedding_provider.py

from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer

from .triage_config import EMBEDDING_MODEL_NAME, EMBEDDING_MODEL_DIR

_embedding_model: SentenceTransformer | None = None


def get_embedding_model() -> SentenceTransformer:
    """
    Lazy-load the MiniLM embedding model once per Python process.
    Reuses the same model folder as workshop2/rag_demo/data/models/.
    """
    global _embedding_model
    if _embedding_model is None:
        print(f"Loading MiniLM embedding model from: {EMBEDDING_MODEL_DIR}")
        EMBEDDING_MODEL_DIR.mkdir(parents=True, exist_ok=True)
        _embedding_model = SentenceTransformer(
            EMBEDDING_MODEL_NAME,
            cache_folder=str(EMBEDDING_MODEL_DIR),
        )
    return _embedding_model


def embed_texts(texts: List[str]) -> np.ndarray:
    """Embed a list of texts into a 2D numpy array: shape (N, D)."""
    model = get_embedding_model()
    return model.encode(texts, convert_to_numpy=True)


def embed_query(text: str) -> np.ndarray:
    """Embed a single query text into a 1D numpy array: shape (D,)."""
    model = get_embedding_model()
    vec = model.encode([text], convert_to_numpy=True)
    return vec[0]
