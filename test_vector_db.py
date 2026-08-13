from utils.vector_db import store_chunks, search
from utils.embeddings import create_embeddings, create_query_embedding

chunks = [
    "Python is a programming language.",
    "Artificial Intelligence is a branch of computer science.",
    "Machine learning is a subset of AI.",
    "Databases store information."
]

embeddings = create_embeddings(chunks)

store_chunks(chunks, embeddings)

query = create_query_embedding("What is AI?")

results = search(query)

print(results)