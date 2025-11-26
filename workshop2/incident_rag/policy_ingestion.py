# workshop2/incident_rag/policy_ingestion.py

from __future__ import annotations

from pathlib import Path
from typing import List

from .triage_schema import PolicyChunkSchema


def load_raw_policy_text(path: Path) -> str:
    """
    Load policy text from a file.
    For simplicity, we treat .txt and .md as UTF-8 text.
    You can extend this to PDF/Word in real-world use cases.
    """
    if not path.exists():
        raise FileNotFoundError(f"Policy file not found: {path}")

    suffix = path.suffix.lower()
    if suffix in {".txt", ".md"}:
        return path.read_text(encoding="utf-8")

    # Simple fallback: treat as text
    return path.read_text(encoding="utf-8", errors="ignore")


def chunk_policy_text(document_name: str, text: str) -> List[PolicyChunkSchema]:
    """
    Very simple chunking: split on double newlines.
    In a real system, you might split by headings or sections.
    """
    chunks: List[PolicyChunkSchema] = []
    raw_sections = [s.strip() for s in text.split("\n\n") if s.strip()]

    for idx, section in enumerate(raw_sections):
        section_id = f"{document_name}#sec{idx+1}"
        section_path = f"Section {idx+1}"
        chunks.append(
            PolicyChunkSchema(
                id=section_id,
                document_name=document_name,
                section_path=section_path,
                text=section,
            )
        )

    return chunks
