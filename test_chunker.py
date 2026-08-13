from utils.chunker import split_text

text = "Hello World! " * 100

chunks = split_text(text)

print("Number of chunks:", len(chunks))

print()

print(chunks[0])

print()

print(chunks[1])