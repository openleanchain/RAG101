# workshop2/incident_rag/triage_service.py

from __future__ import annotations

from typing import List

from .triage_schema import PolicyChunkSchema, TriageResultSchema
from .policy_retriever import search_policies
from .triage_prompt import build_triage_messages
from .triage_llm import call_triage_llm
from .audit_log import append_triage_record


def triage_incident(
    incident_text: str,
    top_k: int = 3,
) -> TriageResultSchema:
    """
    High-level API:
    - retrieve relevant policies
    - build grounded prompt
    - call LLM for structured JSON
    - log the decision
    - return TriageResultSchema
    """
    # 1) Retrieve policies
    policy_results = search_policies(incident_text, top_k=top_k)
    policy_chunks: List[PolicyChunkSchema] = [pr[0] for pr in policy_results]

    # 2) Build messages
    messages = build_triage_messages(incident_text, policy_chunks)

    # 3) Call LLM
    llm_result = call_triage_llm(messages)

    # 4) Log
    append_triage_record(incident_text, policy_chunks, llm_result)

    # 5) Map to TriageResultSchema
    data = llm_result.get("data") or {}
    triage = TriageResultSchema(
        summary=data.get("summary", ""),
        severity=data.get("severity", ""),
        actions_now=data.get("actions_now", []) or [],
        next_steps=data.get("next_steps", []) or [],
        requires_policy_update=bool(data.get("requires_policy_update", False)),
        policy_refs=data.get("policy_refs", []) or [],
    )
    return triage
