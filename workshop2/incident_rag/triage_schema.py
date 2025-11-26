# workshop2/incident_rag/triage_schema.py

from dataclasses import dataclass
from typing import List


@dataclass
class PolicyChunkSchema:
    """One chunk/section of a policy document in the knowledge base."""
    id: str
    document_name: str
    section_path: str
    text: str


@dataclass
class TriageResultSchema:
    """
    Structured triage result from the LLM.
    Mirrors the JSON schema used in Workshop 1 (GenAI 101)
    but now grounded in policies via RAG.
    """
    summary: str
    severity: str                 # "NORMAL" | "ALERT" | "CRISIS"
    actions_now: List[str]
    next_steps: List[str]
    requires_policy_update: bool
    policy_refs: List[str]
