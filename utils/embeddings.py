from sklearn.feature_extraction.text import TfidfVectorizer


# Store the vectorizer so it can be reused
vectorizer = TfidfVectorizer(
    stop_words="english"
)


def create_embeddings(chunks):
    """
    Convert PDF chunks into lightweight TF-IDF vectors.
    """

    embeddings = vectorizer.fit_transform(chunks)

    return embeddings


def create_query_embedding(query):
    """
    Convert the user's question into the same
    TF-IDF representation used for the PDF chunks.
    """

    embedding = vectorizer.transform([query])

    return embedding