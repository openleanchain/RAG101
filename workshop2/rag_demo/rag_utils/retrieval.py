"""
retrieval.py

Retrieval step: find the top-k most similar knowledge cards
for a given question.

For kids:
- "We give the question its own number code."
- "We ask: which cards are closest friends with this question?"
"""

from typing import Any, Dict, List

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

from .rag_config import TOP_K, EMBEDDING_MODEL_NAME
from .knowledge_library import load_knowledge_library, get_embedding_model


def encode_query(question: str) -> np.ndarray:
    """
    Turn the question into an embedding using the same model
    as the knowledge cards.
    """
    model: SentenceTransformer = get_embedding_model()
    vec = model.encode([question], convert_to_numpy=True)
    return vec  # shape: (1, dim)


def retrieve_top_k_cards(
    question: str,
    library: Dict[str, Any] | None = None,
    top_k: int = TOP_K,
) -> List[Dict[str, Any]]:
    """
    Find the top-k most similar knowledge cards for a question.

    If 'library' is not provided, it will be loaded from disk.
    """
    if library is None:
        library = load_knowledge_library()

    cards = library["cards"]
    card_embeddings = np.array([c["embedding"] for c in cards])

    question_vec = encode_query(question)

    # Cosine similarity: higher score = more similar
    sims = cosine_similarity(question_vec, card_embeddings)[0]
    indices = np.argsort(sims)[::-1]  # sort high → low

    top_indices = indices[:top_k]
    top_cards: List[Dict[str, Any]] = []

    for idx in top_indices:
        card = cards[int(idx)].copy()
        card["similarity"] = float(sims[int(idx)])
        top_cards.append(card)

    return top_cards
