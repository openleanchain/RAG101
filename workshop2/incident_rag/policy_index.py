# workshop2/incident_rag/policy_index.py

from __future__ import annotations

import json
from pathlib import Path
from typing import List, Tuple

import numpy as np

from .triage_config import POLICIES_DIR, INDEX_DIR
from .triage_schema import PolicyChunkSchema
from .policy_ingestion import load_raw_policy_text, chunk_policy_text
from .embedding_provider import embed_texts


CHUNKS_JSON_PATH = INDEX_DIR / "policy_chunks.json"
EMBEDDINGS_NPZ_PATH = INDEX_DIR / "policy_embeddings.npz" # NumPy compressed archive format


def build_policy_chunks() -> List[PolicyChunkSchema]:
    """Load all policy files and chunk them into PolicyChunkSchema objects."""
    chunks: List[PolicyChunkSchema] = []

    for path in sorted(POLICIES_DIR.glob("*")):
        if not path.is_file():
            continue
        doc_name = path.name
        print(f"Processing policy: {doc_name}")
        text = load_raw_policy_text(path)
        doc_chunks = chunk_policy_text(doc_name, text)
        chunks.extend(doc_chunks)

    print(f"Total chunks built: {len(chunks)}")
    return chunks


def save_policy_index(
    chunks: List[PolicyChunkSchema],
    embeddings: np.ndarray,
) -> None:
    """Save chunks metadata + embeddings to disk."""
    INDEX_DIR.mkdir(parents=True, exist_ok=True)

    # Save chunk metadata
    serializable = [
        {
            "id": c.id,
            "document_name": c.document_name,
            "section_path": c.section_path,
            "text": c.text,
        }
        for c in chunks
    ]
    CHUNKS_JSON_PATH.write_text(json.dumps(serializable, indent=2), encoding="utf-8")

    # Save embeddings separately: Creates a compressed .npz file (smaller on disk).
    np.savez_compressed(EMBEDDINGS_NPZ_PATH, embeddings=embeddings)
    print(f"Saved chunks to {CHUNKS_JSON_PATH}")
    print(f"Saved embeddings to {EMBEDDINGS_NPZ_PATH}")


def load_policy_index() -> Tuple[List[PolicyChunkSchema], np.ndarray]:
    """Load chunk metadata + embeddings from disk."""
    if not CHUNKS_JSON_PATH.exists() or not EMBEDDINGS_NPZ_PATH.exists():
        raise FileNotFoundError(
            "Policy index not found. Run the index build (Ex04) first."
        )

    data = json.loads(CHUNKS_JSON_PATH.read_text(encoding="utf-8"))
    chunks: List[PolicyChunkSchema] = [
        PolicyChunkSchema(
            id=item["id"],
            document_name=item["document_name"],
            section_path=item["section_path"],
            text=item["text"],
        )
        for item in data
    ]

    npz = np.load(EMBEDDINGS_NPZ_PATH)
    embeddings = npz["embeddings"]
    return chunks, embeddings


def build_and_save_policy_index() -> None:
    """One-shot helper for Ex04: build chunks, embed, save index."""
    chunks = build_policy_chunks()
    texts = [c.text for c in chunks]
    embeddings = embed_texts(texts)
    save_policy_index(chunks, embeddings)
