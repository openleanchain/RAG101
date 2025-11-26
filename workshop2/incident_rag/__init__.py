# workshop2/incident_rag/__init__.py

"""
incident_rag: Enterprise RAG package for Workshop 2

Provides:
- triage_config: paths, model settings
- triage_schema: data schemas (policy chunks, triage result)
- embedding_provider: MiniLM/Azure embedding wrapper
- policy_ingestion: load + chunk policy documents
- policy_index: build & save/load vectorized knowledge base
- policy_retriever: embedding-based retrieval
- triage_prompt: build grounded prompt from templates
- triage_llm: call LLM to get structured JSON triage result
- triage_service: one-stop triage_incident() API
- audit_log: JSONL audit log (long-term memory)
"""
