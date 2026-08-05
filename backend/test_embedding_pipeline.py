from parser.pdf_parser import extract_text_from_pdf
from parser.cleaner import clean_text
from parser.line_splitter import split_into_lines
from parser.line_classifier import classify_lines
from parser.block_detector import detect_blocks

from retrieval.chunker import create_chunks

from embeddings.service import embed_chunks


def main():

    # -----------------------------
    # Parse Resume
    # -----------------------------
    parsed_resume = extract_text_from_pdf(
        "uploads/sample_resume.pdf"
    )

    if not parsed_resume["success"]:
        print(parsed_resume["error"])
        return

    parsed_resume["text"] = clean_text(
        parsed_resume["text"]
    )

    # -----------------------------
    # Build Resume Pipeline
    # -----------------------------
    lines = split_into_lines(parsed_resume)

    document_lines = classify_lines(lines)

    blocks = detect_blocks(document_lines)

    chunks = create_chunks(blocks)

    embedded_chunks = embed_chunks(chunks)

    # -----------------------------
    # Print Results
    # -----------------------------
    print()

    print(f"Total Embedded Chunks : {len(embedded_chunks)}")

    print()

    for chunk in embedded_chunks:

        print("=" * 70)

        print(f"Chunk ID : {chunk.chunk_id}")

        print(f"Section  : {chunk.section}")

        print(f"Subsection : {chunk.subsection}")

        print(f"Embedding Dimension : {len(chunk.embedding)}")

        print()

        print("First 5 Values:")

        print(chunk.embedding[:5])

        print()


if __name__ == "__main__":
    main()