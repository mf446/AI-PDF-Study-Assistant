from sentence_transformers import SentenceTransformer

# Load the model only once
model = SentenceTransformer("all-MiniLM-L6-v2")


def create_embeddings(chunks):
    """
    Convert a list of text chunks into embeddings.

    Args:
        chunks (list[str])

    Returns:
        list
    """
    embeddings = model.encode(
        chunks,
        convert_to_numpy=True,
        show_progress_bar=True
    )

    return embeddings


def create_query_embedding(query):
    """
    Convert a user's question into an embedding.
    """

    embedding = model.encode(
        query,
        convert_to_numpy=True
    )

    return embedding