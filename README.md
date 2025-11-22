# IT Repair Hero Academy — RAG 101

**Purpose:** This repository stores the **training content** for a follow-up course on **RAG 101: Retrieval-Augmented Generation (RAG)**. We build on Workshop 1 and show how to **use internal policies and procedures as an AI knowledge base**, so responses are grounded in **enterprise rules**, not just generic model knowledge.

**Audience:** Anyone who has completed GenAI 101.

**Install:** Environment setup (Python, virtual env, MiniLM model, etc.) is covered in the **`rag_demo` README**.  
Workshop 2 **reuses the same environment and embedding model**—no new setup is required beyond that.

---

## Your Mission Objectives

Use these as the four learning pillars for Workshop 2.

- **Knowledge Base Builder** — *Turn internal policies and procedures into a searchable, vectorized knowledge base that AI can understand and reuse.*  
- **Relevant Info Retriever** — *Use embedding search to pull back the most relevant policy sections for any incident or query.*  
- **Grounded Prompt Designer** — *Build augmented (grounded) prompts that feed the right policy snippets into the LLM so answers follow enterprise rules.*  
- **Integration & Improvement Hero** — *Produce structured outputs that plug into existing systems (the GenAI 101 app, ticketing tools, dashboards) and log everything for audit and continuous improvement.*

---

## Course Map

1. **🎯 Introduction & Recap**  
   **What you do:** Connect Workshop 1 (GenAI 101) with Workshop 2. Review the IT incident triage storyline (“Tech Core needs rescue”) and introduce the idea of an **enterprise knowledge base** and **RAG**.  
   **Outcome:** Understand how we move from “LLM-only decisions” to **LLM + internal policies**, and how this pattern generalizes beyond triage.

2. **📚 Build the Knowledge Base**  
   **Focus:** Turn raw policy documents into structured **policy chunks** and **vector embeddings** using the same MiniLM model from the `rag_demo`.  
   **Outcome:** Learn how to **build a domain-specific, vectorized knowledge base** from enterprise content that can be indexed, searched, and reused.

3. **🔍 Retrieve What Matters**  
   **Focus:** Implement **embedding-based retrieval**: given an incident description (e.g., “VPN down after hours”), find the **top-K most relevant policy sections**.  
   **Outcome:** Be able to **retrieve the right pieces of internal knowledge** on demand, a pattern you can reuse for Q&A, documentation assistants, and support tools.

4. **🧱 Augmented Prompt & JSON Triage**  
   **Focus:** Use **prompt templates** (system/user `.txt` files) to build an **augmented / grounded prompt** that combines:  
   - relevant policy snippets,  
   - the incident description, and  
   - clear instructions for a **structured JSON triage result** (summary, severity, actions, next steps).  
   **Outcome:** Generate **policy-aligned, structured answers** that are traceable back to specific documents, not hallucinated.

5. **🔗 Service Integration & Long-Term Memory**  
   **Focus:** Wrap the RAG pipeline into a `triage_service` API and store each decision in a **JSONL audit log** (long-term memory). Discuss how this could plug into the **existing GenAI 101 app**, ticketing systems, or dashboards.  
   **Outcome:** Understand how to **integrate RAG into real systems**, reuse the same pattern for other domains, and keep a history for audit, analytics, and improvements.

6. **🚀 Extensions, Next Steps & Graduate**  
   **Focus:** Explore next steps: vector databases, **Azure AI Search**, index refresh strategies, and guardrails (e.g., enforcing severity enums, requiring policy references).  
   **Outcome:** See how the triage example is just one instance of a **broader enterprise RAG pattern** that can be applied to HR, finance, operations, and more.

---

## Repository Structure

```text
/setup                 # (from Workshop 1) Python + VS Code environment helpers
/webapp                # (from Workshop 1) GenAI 101 baseline web app
/workshop1             # Workshop 1: GenAI 101 Beyond Chatbot (prompts, JSON, tools)
workshop2/
  ├─ rag_demo/         # Kids-style RAG demo used for pre-work and environment/model setup
  ├─ incident_rag/     # Enterprise RAG package: knowledge base, retrieval, triage service
  ├─ data/             # Sample policies, index storage, prompt templates and JSONL audit logs
  └─ exercises/        # Step-by-step Python exercises (Ex01–Ex08)
```

