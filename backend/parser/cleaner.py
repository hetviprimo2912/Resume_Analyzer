import re


def clean_text(text: str) -> str:
    """
    Clean extracted PDF text before chunking.

    Steps:
    1. Normalize line endings
    2. Remove tabs
    3. Remove extra spaces
    4. Remove excessive blank lines
    5. Trim leading/trailing whitespace
    """

    if not text:
        return ""

    # Normalize line endings
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Replace tabs with spaces
    text = text.replace("\t", " ")

    # Collapse multiple spaces
    text = re.sub(r"[ ]{2,}", " ", text)

    # Collapse multiple blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Strip leading/trailing whitespace
    text = text.strip()

    return text