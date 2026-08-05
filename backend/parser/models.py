from dataclasses import dataclass
from enum import Enum


class LineType(Enum):
    """
    Represents the type of a line extracted from a document.
    """

    HEADER = "HEADER"
    CONTENT = "CONTENT"
    EMAIL = "EMAIL"
    PHONE = "PHONE"
    URL = "URL"
    EMPTY = "EMPTY"


@dataclass
class DocumentLine:
    page: int
    line_number: int
    text: str
    line_type: LineType
    confidence: float = 1.0

@dataclass
class ResumeBlock:
    """
    Represents one logical block of a document.
    """

    block_id: int
    page: int
    title: str
    lines: list[DocumentLine]


@dataclass
class ResumeChunk:
    """
    Represents one semantic chunk that will be embedded.
    """

    chunk_id: int

    page: int

    section: str

    subsection: str | None

    content: str

    character_count: int
    
@dataclass
class ResumeEmbedding:
    """
    Represents one embedded resume chunk.
    """

    chunk_id: int

    page: int

    section: str

    subsection: str | None

    content: str

    character_count: int

    embedding: list[float]