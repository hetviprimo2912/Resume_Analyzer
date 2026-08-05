from parser.pdf_parser import extract_text_from_pdf
from parser.cleaner import clean_text
from parser.line_splitter import split_into_lines
from parser.line_classifier import classify_lines
from parser.block_detector import detect_blocks

from retrieval.chunker import create_chunks


def main():

    parsed_resume = extract_text_from_pdf(
        "uploads/sample_resume.pdf"
    )

    parsed_resume["text"] = clean_text(
        parsed_resume["text"]
    )

    lines = split_into_lines(parsed_resume)

    document_lines = classify_lines(lines)

    blocks = detect_blocks(document_lines)

    chunks = create_chunks(blocks)

    print(f"\nTotal Chunks : {len(chunks)}\n")

    for chunk in chunks:

        print("=" * 60)

        print(f"Chunk ID     : {chunk.chunk_id}")
        print(f"Section      : {chunk.section}")
        print(f"Subsection   : {chunk.subsection}")
        print(f"Characters   : {chunk.character_count}")

        print("-" * 60)

        print(chunk.content)

        print()


if __name__ == "__main__":
    main()