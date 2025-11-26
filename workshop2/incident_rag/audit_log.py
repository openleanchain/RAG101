# workshop2/incident_rag/audit_log.py

from __future__ import annotations

import json
from datetime import datetime
from typing import Any, Dict, List

from .triage_config import LOGS_DIR
from .triage_schema import PolicyChunkSchema

LOG_PATH = LOGS_DIR / "triage_log.jsonl"


def append_triage_record(
    incident_text: str,
    policy_chunks: List[PolicyChunkSchema],
    llm_result: Dict[str, Any],
) -> None:
    """
    Append one triage record to triage_log.jsonl.
    This is our long-term memory / audit log.
    """
    record = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "incident_text": incident_text,
        "policy_chunks": [
            {
                "id": c.id,
                "document_name": c.document_name,
                "section_path": c.section_path,
            }
            for c in policy_chunks
        ],
        "triage_data": llm_result.get("data"),
        "usage": llm_result.get("usage"),
    }

    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")
