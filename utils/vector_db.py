import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


# Stored PDF chunks and their TF-IDF vectors
stored_chunks = []
stored_embeddings = None


def store_chunks(chunks, embeddings):
    """
    Store PDF chunks and their TF-IDF vectors.
    """

    global stored_chunks, stored_embeddings

    stored_chunks = chunks
    stored_embeddings = embeddings


def search(query_embedding, top_k=10):
    """
    Return the most relevant PDF chunks using
    cosine similarity.
    """

    if not stored_chunks or stored_embeddings is None:
        return []

    # Calculate similarity between the question
    # and every PDF chunk
    similarities = cosine_similarity(
        query_embedding,
        stored_embeddings
    )[0]

    # Get the indexes of the most relevant chunks
    top_indexes = np.argsort(similarities)[::-1][:top_k]

    results = [
        stored_chunks[i]
        for i in top_indexes
    ]

    print("\n========== Retrieved Chunks ==========\n")

    for i, chunk in enumerate(results, start=1):
        print(f"Chunk {i}:")
        print(chunk[:300])
        print("\n----------------------------\n")

    return results