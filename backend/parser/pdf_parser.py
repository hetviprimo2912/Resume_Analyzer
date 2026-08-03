import fitz


def extract_text_from_pdf(file_path: str):

    try:

        document = fitz.open(file_path)

        full_text = ""

        pages = []

        for page_number, page in enumerate(document, start=1):

            blocks = page.get_text("blocks")

            # --------------------------------------------------
            # Detect column separator dynamically
            # --------------------------------------------------

            x_positions = sorted(block[0] for block in blocks)

            largest_gap = 0
            separator = 0

            for i in range(len(x_positions) - 1):

                gap = x_positions[i + 1] - x_positions[i]

                if gap > largest_gap:
                    largest_gap = gap
                    separator = (x_positions[i] + x_positions[i + 1]) / 2

            left_column = []
            right_column = []

            for block in blocks:

                x0 = block[0]

                if x0 < separator:
                    left_column.append(block)
                else:
                    right_column.append(block)

            # Sort each column from top to bottom
            left_column.sort(key=lambda b: b[1])
            right_column.sort(key=lambda b: b[1])

            # Reading order:
            # Left column first, then right column
            blocks = left_column + right_column

            page_text = ""
            page_blocks = []

            for block in blocks:

                x0, y0, x1, y1, text, *_ = block

                text = text.strip()

                if not text:
                    continue

                page_blocks.append({
                    "bbox": {
                        "x0": x0,
                        "y0": y0,
                        "x1": x1,
                        "y1": y1
                    },
                    "text": text
                })

                page_text += text + "\n"

            pages.append({
                "page": page_number,
                "text": page_text,
                "blocks": page_blocks
            })

            full_text += page_text + "\n"

        return {
            "success": True,
            "page_count": len(document),
            "character_count": len(full_text),
            "text": full_text,
            "pages": pages
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }