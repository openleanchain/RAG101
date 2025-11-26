# Uses your embedding model (SentenceTransformer MiniLM in your setup) to encode the query into a single vector.
print("=================Loading tools and libraries, may take 1-2 minutes, please wait...")

from workshop2.incident_rag.embedding_provider import embed_query

query = input("\nSearch query: ").strip()
if not query or query.lower() == "q":
    print("Bye.")
else:
    q_vec = embed_query(query)  # q_vec.shape == (384,) → 1D vector.
    q_vec_2d = q_vec.reshape(1, -1)  # reshape from shape (dim,) to (1, dim)
    print(q_vec_2d)
    print(f"Encoded query vector shape: {q_vec.shape}")
    print(f"Reshaped query vector shape: {q_vec_2d.shape}")
