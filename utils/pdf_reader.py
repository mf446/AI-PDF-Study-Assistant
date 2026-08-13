import fitz


def extract_text(file_path):
    """
    Extract all text from a PDF file.
    """

    document = fitz.open(file_path)

    text = ""

    for page in document:
        text += page.get_text()

    document.close()

    return text