"""
memory_store.py

Very simple "long-term memory" for the RAG demo.

Concept:
- Short-term memory = the messages we send to the model in THIS call.
- Long-term memory = a notebook file where OUR APP saves important
  conversation turns so we can look back later.

Implementation:
- Append one JSON record per question/answer into a .jsonl file.
- Format: JSON Lines (one JSON object per line).
"""

import json
from datetime import datetime, timezone
from typing import Any, Dict, List

from .rag_config import CONVERSATION_LOG_PATH


def append_conversation_record(
    question: str,
    top_cards: List[Dict[str, Any]],
    llm_data: Dict[str, Any],
    usage: Dict[str, Any],
) -> None:
    """
    Append one conversation record to the long-term memory log.

    Stored fields:
    - timestamp_utc : ISO-8601 timestamp in UTC
    - question      : the student's question
    - used_cards    : list of {id, page, similarity} for transparency
    - llm_data      : JSON data returned by the model (e.g. answer, sources)
    - usage         : token usage (prompt/completion/total)

    File:
    - CONVERSATION_LOG_PATH (JSONL: one JSON object per line)
    """
    record = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "question": question,
        "used_cards": [
            {
                "id": c.get("id"),
                "page": c.get("page"),
                "similarity": c.get("similarity"),
            }
            for c in top_cards
        ],
        "llm_data": llm_data,
        "usage": usage,
    }

    # Ensure parent folder exists (should already, but this is safe)
    CONVERSATION_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Append as one JSON line
    with CONVERSATION_LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False))
        f.write("\n")
