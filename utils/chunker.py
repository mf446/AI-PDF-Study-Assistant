import re


def split_text(text, chunk_size=1000, overlap=300):
    """
    Split PDF text into chunks while trying to preserve
    sentences and paragraphs.
    """

    # Clean excessive spaces
    text = re.sub(r'[ \t]+', ' ', text)

    # Normalize line breaks
    text = re.sub(r'\n+', '\n', text)

    # Split text into sentences
    sentences = re.split(
        r'(?<=[.!?])\s+',
        text
    )

    chunks = []
    current_chunk = ""

    for sentence in sentences:

        sentence = sentence.strip()

        if not sentence:
            continue

        # If adding the sentence keeps the chunk
        # within the desired size
        if len(current_chunk) + len(sentence) + 1 <= chunk_size:

            if current_chunk:
                current_chunk += " "

            current_chunk += sentence

        else:

            # Save current chunk
            if current_chunk:
                chunks.append(
                    current_chunk
                )

            # Start a new chunk
            current_chunk = sentence


    # Add the final chunk
    if current_chunk:
        chunks.append(
            current_chunk
        )


    # Add overlap
    final_chunks = []

    for i, chunk in enumerate(chunks):

        if i == 0:

            final_chunks.append(
                chunk
            )

        else:

            previous_chunk = chunks[i - 1]

            overlap_text = previous_chunk[
                -overlap:
            ]

            combined_chunk = (
                overlap_text
                + " "
                + chunk
            )

            final_chunks.append(
                combined_chunk
            )


    return final_chunks