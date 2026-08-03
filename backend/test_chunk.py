from parser.pdf_parser import extract_text_from_pdf
from parser.cleaner import clean_text
from parser.line_splitter import split_into_lines
from parser.line_classifier import classify_lines
from parser.block_detector import detect_blocks

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

    print(f"\nTotal Blocks : {len(blocks)}\n")

    for block in blocks:

        print("=" * 70)

        print(f"Block : {block.block_id}")

        print(f"Title : {block.title}")

        print(f"Page  : {block.page}")

        print("-" * 70)

        for line in block.lines:
            print(line.text)

        print()

if __name__ == "__main__":
    main()