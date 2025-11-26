# workshop2/exercises/ex07_rag_triage_llm_json.py
print("=================Loading tools and libraries, may take 1-2 minutes, please wait...")

import json
from workshop2.incident_rag.policy_retriever import search_policies
from workshop2.incident_rag.triage_prompt import build_triage_messages
from workshop2.incident_rag.triage_llm import call_triage_llm


def main() -> None:
    print("=== Ex07: RAG triage LLM (JSON result) ===")
    print("Paste an incident description (or 'q' to quit).")

    while True:
        incident = input("\nIncident: ").strip()
        if not incident or incident.lower() == "q":
            print("Bye.")
            break

        # 1) Retrieve policies
        policy_results = search_policies(incident, top_k=3)
        policy_chunks = [pr[0] for pr in policy_results]
        if not policy_chunks:
            print("No relevant policies found.")
            continue

        # 2) Build messages
        messages = build_triage_messages(incident, policy_chunks)

        # 3) Call LLM
        llm_result = call_triage_llm(messages)

        print("\n--- LLM JSON result ---")
        print(json.dumps(llm_result.get("data"), indent=2))
        print("\nUsage:", llm_result.get("usage"))


if __name__ == "__main__":
    main()
