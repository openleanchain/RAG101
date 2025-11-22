# IT Repair Hero Academy — RAG 101

**Purpose:** This repository stores the **training content** for a follow-up course on **RAG 101: Retrieval-Augmented Generation (RAG)**. We build on Workshop 1 (GenAI 101 Beyond Chatbot) and show how to **use internal policies and procedures as an AI knowledge base**, so responses are grounded in **enterprise rules**, not just generic model knowledge.

**Audience:** Anyone who has completed GenAI 101.

**Install:** Environment setup (Python, virtual env, MiniLM model, etc.) is covered in the **`rag_demo` README**.  
Workshop 2 **reuses the same environment and embedding model**—no new setup is required beyond that.

---

## Your Mission Objectives

Use these as the four learning pillars for Workshop 2.

- **Knowledge Base Builder** — *Turn internal policies and procedures into a searchable, vectorized knowledge base that AI can understand and reuse.*  
- **Relevant Info Retriever** — *Use embedding search to pull back the most relevant policy sections for any incident or query.*  
- **Augmented Prompt Designer** — *Build augmented (grounded) prompts that feed the right policy snippets into the LLM so answers follow enterprise rules.*  
- **Integration & Improvement Hero** — *Generate structured outputs that plug into existing systems (the GenAI 101 app, ticketing tools, dashboards) and log everything for audit and continuous improvement.*

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

6. **🎓 Graduation — From Triage to Enterprise Patterns (RAG Hero)**  
   **Focus:** Wrap-up, reflection, and a look beyond the single triage use case into **enterprise-wide RAG patterns**.  
   **What you do:**  
   - Review the full pipeline you built: knowledge base → retrieval → grounded prompt templates → structured triage JSON → audit log.  
   - Compare the original GenAI 101 “LLM-only” triage with the new **RAG-powered triage** and discuss how the quality of decisions improved.  
   - Explore extensions: using **vector databases** or **Azure AI Search**, using hybrid search to improve retrieval accuracy in real-world enterprise scenarios, planning index refresh when policies change, and adding guardrails (e.g., enforcing severity enums, requiring policy references, forcing escalation when no relevant policy is found).
   - Complete the capstone and an 8‑question quiz (≈2 per section) to earn a certificate.
   
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
  ├─ data/
  │   ├─ policies/        # Sample policies and procedures
  │   ├─ index/           # Saved vector index / knowledge base artifacts
  │   ├─ prompts/         # System/user prompt templates for grounded triage
  │   └─ logs/            # JSONL audit logs (long-term memory)
  └─ exercises/        # Step-by-step Python exercises (Ex01–Ex08)
```
**Note**:
- `rag_demo` has its own README explaining how to set up the environment and download the MiniLM embedding model.
- `incident_rag` reuses the same embedding model folder and focuses on enterprise patterns, not basic setup.

---

## How to Use This Repo

- Make sure you have completed the `rag_demo` setup under `workshop2/rag_demo` and can run the RAG demo.
- Open the `workshop2/incident_rag`, `workshop2/data`, and `workshop2/exercises` folders in VS Code.
- Follow the exercises in order (Ex01 → Ex08). Each script is stand-alone runnable, but builds on a common set of modules:
  - build the knowledge base,
  - retrieve relevant policies,
  - construct grounded prompts from `data/prompts/`,
  - call the LLM for structured triage,
  - and log decisions for long-term memory in `data/logs/`.

---
 
## Progress & Gamification

As in Workshop 1, progression is broken into **small, visible steps**:
- Each exercise Ex01–Ex08 has a clear goal and “done” signal (e.g., a printed summary, a successful search, a JSON triage result, a new log entry).
- Learners can see their progress from:
  - “I can load policies” → “I can search them” → “I can drive an LLM with them” → “I can expose a triage service with an audit trail.”
- Optional challenges:
  - add a new policy document to the knowledge base,
  - tune `top_k` retrieval or prompt wording to improve answer quality,
  - imagine how the same pattern could support another domain (HR, finance, support).

The final goal is a working **RAG-powered triage service** that feels like a “Version 2” of the Workshop 1 app: the same IT emergency storyline, but now **backed by your own knowledge base**, and a “**RAG Hero**” certificate to match your “**IT Repair Hero**” badge from Workshop 1.

---

## License

Use a permissive license (e.g., **MIT**) to encourage educational reuse. Add `LICENSE` at the project root.
