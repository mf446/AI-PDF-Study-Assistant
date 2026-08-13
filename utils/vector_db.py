import chromadb

# Create a local database
client = chromadb.Client()

# Create (or reuse) a collection
collection = client.get_or_create_collection(
    name="pdf_chunks"
)


def store_chunks(chunks, embeddings):
    """
    Store text chunks and their embeddings.
    """

    # Remove old PDF data
    try:
        collection.delete(
            ids=[str(i) for i in range(collection.count())]
        )
    except Exception:
        pass

    collection.add(
        ids=[str(i) for i in range(len(chunks))],
        documents=chunks,
        embeddings=embeddings.tolist()
    )


def search(query_embedding, top_k=10):
    """
    Return the most relevant chunks.
    """

    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=top_k
    )

    print("\n========== Retrieved Chunks ==========\n")

    for i, chunk in enumerate(results["documents"][0], start=1):
        print(f"Chunk {i}:")
        print(chunk[:300])   # Print first 300 characters
        print("\n----------------------------\n")

    return results["documents"][0]