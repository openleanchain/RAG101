# workshop2/exercises/ex03_embed_policy_chunks.py
print("=================Loading tools and libraries, may take 1-2 minutes, please wait...")
from workshop2.incident_rag.triage_config import POLICIES_DIR
from workshop2.incident_rag.policy_ingestion import load_raw_policy_text, chunk_policy_text
from workshop2.incident_rag.embedding_provider import embed_texts


def main() -> None:
    print("=== Ex03: Embed policy chunks (in memory) ===")

    policy_files = sorted(POLICIES_DIR.glob("*"))
    if not policy_files:
        print(f"No policy files found in {POLICIES_DIR}.")
        return

    all_texts = []
    for path in policy_files:
        if not path.is_file():
            continue
        # ex01
        text = load_raw_policy_text(path)
        # ex02
        chunks = chunk_policy_text(path.name, text)
        print(f"\n--- {path.name} --- Total chunks: {len(chunks)}")
        all_texts.extend(c.text for c in chunks)

    if not all_texts:
        print("No chunks to embed.")
        return

    print(f"Embedding {len(all_texts)} chunks...")
    # create embeddings for all the text chunks
    embeddings = embed_texts(all_texts)
    print(f"Embeddings shape: {embeddings.shape}")
    print("Sample embedding (first line):")
    print(embeddings[0])
    print(f"{len(embeddings[0])} dimensions")
    print("Done. (In later exercises, we'll save these as an index.)")


if __name__ == "__main__":
    main()
