from typing import List, Tuple


def split_into_lines(parsed_resume) -> List[Tuple[int, str]]:
    """
    Splits each visual block into individual lines.

    Returns:
        [
            (page_number, line),
            ...
        ]
    """

    lines = []

    for page in parsed_resume["pages"]:

        page_number = page["page"]

        # Iterate over visual blocks instead of full page text
        for block in page["blocks"]:

            block_lines = block["text"].splitlines()

            for line in block_lines:

                line = line.strip()

                if line:
                    lines.append((page_number, line))

    return lines