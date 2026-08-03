from parser.pdf_parser import extract_text_from_pdf
from parser.cleaner import clean_text


PDF_PATH = "uploads/sample_resume.pdf"


def main():
    result = extract_text_from_pdf(PDF_PATH)

    if not result["success"]:
        print(result["error"])
        return

    raw_text = result["text"]

    clean = clean_text(raw_text)

    print("=" * 80)
    print("RAW TEXT")
    print("=" * 80)
    print(raw_text[:1200])

    print("\n\n")

    print("=" * 80)
    print("CLEAN TEXT")
    print("=" * 80)
    print(clean[:1200])


if __name__ == "__main__":
    main()