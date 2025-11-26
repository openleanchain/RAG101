# workshop2/incident_rag/triage_prompt.py

from __future__ import annotations

from pathlib import Path
from typing import List, Dict, Any

from .triage_config import PROMPTS_DIR
from .triage_schema import PolicyChunkSchema

_SYSTEM_PROMPT_NAME = "triage_system_prompt_template.txt"
_USER_PROMPT_NAME = "triage_user_prompt_template.txt"

_cached_system: str | None = None
_cached_user: str | None = None


def _load_prompt(name: str) -> str:
    path = PROMPTS_DIR / name
    if not path.exists():
        raise FileNotFoundError(
            f"Prompt template not found: {path}. "
            f"Create it under data/prompts/."
        )
    return path.read_text(encoding="utf-8")


def get_system_prompt() -> str:
    global _cached_system
    if _cached_system is None:
        _cached_system = _load_prompt(_SYSTEM_PROMPT_NAME)
    return _cached_system


def get_user_prompt_template() -> str:
    global _cached_user
    if _cached_user is None:
        _cached_user = _load_prompt(_USER_PROMPT_NAME)
    return _cached_user


def build_policy_context(chunks: List[PolicyChunkSchema]) -> str:
    """
    Convert top policy chunks into a plain-text context block.
    """
    parts: List[str] = []
    for c in chunks:
        header = f"[{c.document_name} / {c.section_path}]"
        parts.append(f"{header}\n{c.text}")
    return "\n\n".join(parts)


def build_triage_messages(
    incident_text: str,
    policy_chunks: List[PolicyChunkSchema],
) -> List[Dict[str, Any]]:
    """
    Build messages for LLM call using system + user templates.
    The user template should include placeholders like:
      {policy_context}
      {incident_text}
    """
    system_prompt = get_system_prompt()
    user_template = get_user_prompt_template()
    policy_context = build_policy_context(policy_chunks)

    # Python string formatting method that replaces placeholders
    user_content = user_template.format(
        policy_context=policy_context,
        incident_text=incident_text,
    )

    messages: List[Dict[str, Any]] = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_content},
    ]
    return messages
