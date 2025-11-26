# workshop2/exercises/ex02_chunk_policy_sections.py

from workshop2.incident_rag.triage_config import POLICIES_DIR
from workshop2.incident_rag.policy_ingestion import load_raw_policy_text, chunk_policy_text


def main() -> None:
    print("=== Ex02: Chunk policy into sections ===")

    policy_files = sorted(POLICIES_DIR.glob("*"))
    if not policy_files:
        print(f"No policy files found in {POLICIES_DIR}.")
        return

    for path in policy_files:
        if not path.is_file():
            continue
        doc_name = path.name
        print(f"\nProcessing {doc_name}")
        # ex01: extract text from a file
        text = load_raw_policy_text(path)
        # ex02: split the long text into chunks
        chunks = chunk_policy_text(doc_name, text)
        print(f"Total chunks: {len(chunks)}")
        if chunks:
            for chunk in chunks:
                print("\nExample chunk:")
                print(f"ID: {chunk.id}")
                print(f"Section: {chunk.section_path}")
                print(f"Text:\n{chunk.text}")
        break  # show only the first file for this exercise


if __name__ == "__main__":
    main()
