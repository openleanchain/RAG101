"""
knowledge_library.py

Builds and loads the AI Knowledge Library from a PDF.

Pipeline:
1) Read PDF pages.
2) Build knowledge cards (chunks).
3) Compute embeddings for each card.
4) Save everything to knowledge_library.json.
"""

from __future__ import annotations
import json
import os
from typing import Any, Dict, List
import numpy as np
from sentence_transformers import SentenceTransformer

from .rag_config import (
    MODEL_DIR, PDF_PATH,
    KNOWLEDGE_LIBRARY_PATH,
    EMBEDDING_MODEL_NAME,
)
from .pdf_utils import extract_pages_from_pdf, build_knowledge_cards

# Simple embedding model cache so we only load MiniLM once per process
#_embedding_model: SentenceTransformer | None = None
_embedding_model = None

def get_embedding_model() -> SentenceTransformer:
    global _embedding_model
    if _embedding_model is None:
        cache_dir = MODEL_DIR
        cache_dir.mkdir(exist_ok=True)
        _embedding_model = SentenceTransformer(
            EMBEDDING_MODEL_NAME,
            cache_folder=str(cache_dir),
        )
    return _embedding_model


def embed_texts(texts: List[str]) -> np.ndarray:
    """
    Turn a list of texts into a matrix of embeddings.
    """
    model = get_embedding_model()
    embeddings = model.encode(texts, convert_to_numpy=True, show_progress_bar=True)
    return embeddings


def build_and_save_knowledge_library(
    pdf_path=PDF_PATH,
    output_path=KNOWLEDGE_LIBRARY_PATH,
    max_chars_per_chunk: int = 400,
) -> None:
    """
    Full build step:
    - Read PDF pages
    - Build knowledge cards
    - Add embeddings
    - Save as one JSON file (AI Knowledge Library)
    """
    os.makedirs(os.path.dirname(str(output_path)), exist_ok=True)

    print("Step 1: Reading PDF pages...")
    pages = extract_pages_from_pdf(str(pdf_path))
    print(f"  Found {len(pages)} pages with text.")

    print("Step 2: Building knowledge cards (chunks)...")
    cards = build_knowledge_cards(pages, max_chars=max_chars_per_chunk)
    print(f"  Created {len(cards)} knowledge cards.")

    print("Step 3: Embedding cards with MiniLM...")
    texts = [card["text"] for card in cards]
    embeddings = embed_texts(texts)

    for card, emb in zip(cards, embeddings):
        card["embedding"] = emb.tolist()

    library: Dict[str, Any] = {
        "pdf_path": str(pdf_path),
        "embedding_model": EMBEDDING_MODEL_NAME,
        "cards": cards,
    }

    print(f"Saving AI Knowledge Library to {output_path}...")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(library, f, ensure_ascii=False, indent=2)

    print("Done! AI Knowledge Library is ready.")


def load_knowledge_library(
    path=KNOWLEDGE_LIBRARY_PATH,
) -> Dict[str, Any]:
    """
    Load the AI Knowledge Library from JSON.
    """
    with open(path, "r", encoding="utf-8") as f:
        library: Dict[str, Any] = json.load(f)
    return library
