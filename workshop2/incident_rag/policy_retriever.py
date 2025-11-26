# workshop2/incident_rag/policy_retriever.py

from __future__ import annotations

from typing import List, Tuple

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from .triage_schema import PolicyChunkSchema
from .embedding_provider import embed_query
from .policy_index import load_policy_index

# Simple in-memory cache
_cached_chunks: List[PolicyChunkSchema] | None = None
_cached_embeddings: np.ndarray | None = None


def _ensure_index_loaded() -> None:
    global _cached_chunks, _cached_embeddings
    if _cached_chunks is None or _cached_embeddings is None:
        print("Loading policy index from disk...")
        _cached_chunks, _cached_embeddings = load_policy_index()


def search_policies(
    query: str,
    top_k: int = 3,
) -> List[Tuple[PolicyChunkSchema, float]]:
    """
    Given a free-text query (incident description), return top_k
    (PolicyChunkSchema, similarity_score) pairs.
    """
    _ensure_index_loaded()
    assert _cached_chunks is not None
    assert _cached_embeddings is not None

    # Uses your embedding model (SentenceTransformer MiniLM in your setup) to encode the query into a single vector.
    q_vec = embed_query(query)  # q_vec.shape == (384,) → 1D vector.
    q_vec_2d = q_vec.reshape(1, -1)  # reshape from shape (dim,) to (1, dim)
    """
    Each value is the cosine similarity between the query and one chunk:
    1.0 → identical direction (very similar).   
    0 → orthogonal (unrelated).    
    -1 → opposite direction.
    """
    sims = cosine_similarity(q_vec_2d, _cached_embeddings)[0]  # shape (N,)

    # Find the indices of the top-k scores
    top_indices = np.argsort(sims)[::-1][:top_k]  # Reverses that array → descending order (largest first).
    results: List[Tuple[PolicyChunkSchema, float]] = []
    # Map indices back to chunks.
    for idx in top_indices:
        chunk = _cached_chunks[int(idx)]
        score = float(sims[int(idx)])
        results.append((chunk, score))

    return results
