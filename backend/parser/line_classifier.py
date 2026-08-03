

from parser.models import DocumentLine, LineType


from parser.line_rules import (
    is_email,
    is_phone,
    is_url,
    is_spaced_uppercase
)


def classify_line(
    page: int,
    line_number: int,
    text: str
) -> DocumentLine:
    """
    Classify a single extracted line.
    """

    text = text.strip()

    if not text:
        return DocumentLine(
            page=page,
            line_number=line_number,
            text=text,
            line_type=LineType.EMPTY,
            confidence=1.0
        )

    if is_email(text):
        line_type = LineType.EMAIL
        confidence = 1.0

    elif is_phone(text):
        line_type = LineType.PHONE
        confidence = 1.0

    elif is_url(text):
        line_type = LineType.URL
        confidence = 1.0

    elif is_spaced_uppercase(text):
        line_type = LineType.HEADER
        confidence = 0.90

    else:
        line_type = LineType.CONTENT
        confidence = 0.80

    return DocumentLine(
        page=page,
        line_number=line_number,
        text=text,
        line_type=line_type,
        confidence=confidence
    )
    
def classify_lines(lines: list[tuple[int, str]]) -> list[DocumentLine]:
    """
    Convert raw extracted lines into DocumentLine objects.
    """

    classified = []

    for index, (page, text) in enumerate(lines, start=1):

        classified.append(
            classify_line(
                page=page,
                line_number=index,
                text=text
            )
        )

    return classified    