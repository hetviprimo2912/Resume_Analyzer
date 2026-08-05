import uuid

from parser.pdf_parser import extract_text_from_pdf
from parser.cleaner import clean_text
from parser.line_splitter import split_into_lines
from parser.line_classifier import classify_lines
from parser.block_detector import detect_blocks

from retrieval.chunker import create_chunks

from embeddings.service import embed_chunks

from vectorstore.faiss_store import FAISSStore


def index_resume(pdf_path: str) -> str:
    """
    Parse a resume, generate embeddings,
    build a FAISS index and save it.

    Returns:
        resume_id
    """

    # ----------------------------
    # Generate unique Resume ID
    # ----------------------------
    resume_id = str(uuid.uuid4())

    # ----------------------------
    # Parse Resume
    # ----------------------------
    parsed_resume = extract_text_from_pdf(
        pdf_path
    )

    parsed_resume["text"] = clean_text(
        parsed_resume["text"]
    )

    # ----------------------------
    # Create Blocks
    # ----------------------------
    lines = split_into_lines(
        parsed_resume
    )

    document_lines = classify_lines(
        lines
    )

    blocks = detect_blocks(
        document_lines
    )

    # ----------------------------
    # Create Chunks
    # ----------------------------
    chunks = create_chunks(
        blocks
    )

    # ----------------------------
    # Create Embeddings
    # ----------------------------
    embedded_chunks = embed_chunks(
        chunks
    )

    # ----------------------------
    # Build FAISS Store
    # ----------------------------
    store = FAISSStore(384)

    store.add_embeddings(
        embedded_chunks
    )

    # ----------------------------
    # Save Index
    # ----------------------------
    store.save(
        f"storage/{resume_id}"
    )

    return resume_id