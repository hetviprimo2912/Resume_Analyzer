from parser.models import ResumeBlock, DocumentLine, LineType

CONTACT_KEYWORDS = [
    "linkedin",
    "github",
    "portfolio",
    "website",
    "leetcode",
    "hackerrank",
    "codechef",
    "codeforces"
]
def detect_blocks(
    document_lines: list[DocumentLine]
) -> list[ResumeBlock]:
    """
    Groups classified lines into logical resume blocks.
    """

    blocks = []

    block_id = 1

    current_lines = []

    current_page = 1

    current_title = "DOCUMENT"

    pending_header = None

    for line in document_lines:

        # -----------------------------
        # Header detected
        # -----------------------------
        if line.line_type == LineType.HEADER:

            # Save previous block only if it has content
            if current_lines:

                blocks.append(
                    ResumeBlock(
                        block_id=block_id,
                        page=current_page,
                        title=current_title,
                        lines=current_lines
                    )
                )

                block_id += 1

                current_lines = []

            # Don't create a block yet.
            # Just remember the header.
            pending_header = line

            continue

        # -----------------------------
        # Normal content line
        # -----------------------------
        if pending_header is not None:

            current_title = pending_header.text
            current_page = pending_header.page

            pending_header = None

        current_lines.append(line)

    # Save last block
    if current_lines:

        blocks.append(
            ResumeBlock(
                block_id=block_id,
                page=current_page,
                title=current_title,
                lines=current_lines
            )
        )
    # --------------------------------------------------
    # Move LinkedIn / GitHub into CONTACT block
    # --------------------------------------------------

    contact_block = None

    for block in blocks:

        normalized_title = block.title.replace(" ", "").upper()

        if normalized_title == "CONTACT":

            contact_block = block
            break


    if contact_block is not None:

        for block in blocks:

            if block is contact_block:
                continue

            remaining_lines = []

            for line in block.lines:

                text = line.text.lower()

                if any(keyword in text for keyword in CONTACT_KEYWORDS):

                    contact_block.lines.append(line)

                else:

                    remaining_lines.append(line)

            block.lines = remaining_lines


    return blocks