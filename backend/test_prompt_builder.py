from parser.pdf_parser import extract_text_from_pdf
from parser.cleaner import clean_text
from parser.line_splitter import split_into_lines
from parser.line_classifier import classify_lines
from parser.block_detector import detect_blocks

from retrieval.chunker import create_chunks

from embeddings.service import embed_chunks

from vectorstore.faiss_store import FAISSStore

from llm.prompt_builder import build_prompt


def main():

    # -------------------------
    # Parse Resume
    # -------------------------
    parsed_resume = extract_text_from_pdf(
        "uploads/sample_resume.pdf"
    )

    parsed_resume["text"] = clean_text(
        parsed_resume["text"]
    )

    # -------------------------
    # Create Blocks
    # -------------------------
    lines = split_into_lines(parsed_resume)

    document_lines = classify_lines(lines)

    blocks = detect_blocks(document_lines)

    # -------------------------
    # Create Chunks
    # -------------------------
    chunks = create_chunks(blocks)

    # -------------------------
    # Create Embeddings
    # -------------------------
    embedded_chunks = embed_chunks(chunks)

    # -------------------------
    # Build Vector Store
    # -------------------------
    store = FAISSStore(384)

    store.add_embeddings(
        embedded_chunks
    )

    # -------------------------
    # Search
    # -------------------------
    question = "What machine learning projects have you built?"

    matches = store.search(
        query=question,
        top_k=3
    )

    # -------------------------
    # Build Prompt
    # -------------------------
    prompt = build_prompt(
        question=question,
        matches=matches
    )

    print("\n")
    print("=" * 80)
    print("PROMPT SENT TO LLM")
    print("=" * 80)
    print(prompt)


if __name__ == "__main__":
    main()