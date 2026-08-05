from parser.pdf_parser import extract_text_from_pdf
from parser.cleaner import clean_text
from parser.line_splitter import split_into_lines
from parser.line_classifier import classify_lines
from parser.block_detector import detect_blocks

from retrieval.chunker import create_chunks

from embeddings.service import embed_chunks

from vectorstore.faiss_store import FAISSStore


def main():

    # -----------------------------
    # Parse Resume
    # -----------------------------
    parsed_resume = extract_text_from_pdf(
        "uploads/sample_resume.pdf"
    )

    parsed_resume["text"] = clean_text(
        parsed_resume["text"]
    )

    # -----------------------------
    # Create Blocks
    # -----------------------------
    lines = split_into_lines(parsed_resume)

    document_lines = classify_lines(lines)

    blocks = detect_blocks(document_lines)

    # -----------------------------
    # Create Chunks
    # -----------------------------
    chunks = create_chunks(blocks)

    # -----------------------------
    # Generate Embeddings
    # -----------------------------
    embedded_chunks = embed_chunks(chunks)

    # -----------------------------
    # Create FAISS Store
    # -----------------------------
    store = FAISSStore(384)

    store.add_embeddings(
        embedded_chunks
    )

    print()

    print(f"Chunks Created : {len(chunks)}")

    print(f"Embeddings     : {len(embedded_chunks)}")

    print(f"Vectors Stored : {store.index.ntotal}")

    print()


if __name__ == "__main__":
    main()