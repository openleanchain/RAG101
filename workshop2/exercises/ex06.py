# workshop2/exercises/ex06_rag_search_incident.py
print("=================Loading tools and libraries, may take 1-2 minutes, please wait...")

from workshop2.incident_rag.policy_retriever import search_policies


def main() -> None:
    print("=== Ex06: RAG search for incident description ===")
    print("Paste an incident description (or 'q' to quit).")

    while True:
        incident = input("\nIncident: ").strip()
        if not incident or incident.lower() == "q":
            print("Bye.")
            break

        results = search_policies(incident, top_k=3)
        if not results:
            print("No relevant policies found.")
            continue

        print("\nPolicy snippets that would be fed into the LLM:")
        for i, (chunk, score) in enumerate(results, start=1):
            print(f"\n[{i}] Score: {score:.4f}")
            print(f"Doc: {chunk.document_name}")
            print(f"Section: {chunk.section_path}")
            print(f"Text:\n{chunk.text}")


if __name__ == "__main__":
    main()
