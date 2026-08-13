from utils.embeddings import create_embeddings

chunks = [
    "Python is a programming language.",
    "Artificial Intelligence is a branch of computer science.",
    "Databases store information."
]

embeddings = create_embeddings(chunks)

print(type(embeddings))

print()

print(embeddings.shape)