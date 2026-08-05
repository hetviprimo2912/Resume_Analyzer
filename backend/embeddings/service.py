from sentence_transformers import SentenceTransformer

from embeddings.model import get_embedding_model
from parser.models import ResumeChunk, ResumeEmbedding


def embed_text(text: str) -> list[float]:
    """
    Generate an embedding for a single piece of text.
    """

    model: SentenceTransformer = get_embedding_model()

    embedding = model.encode(
        text,
        convert_to_numpy=True
    )

    return embedding.tolist()

def embed_chunks(
    chunks: list[ResumeChunk]
) -> list[ResumeEmbedding]:
    """
    Generate embeddings for all resume chunks.
    """

    embedded_chunks = []

    for chunk in chunks:

        vector = embed_text(chunk.content)

        embedded_chunks.append(

            ResumeEmbedding(

                chunk_id=chunk.chunk_id,

                page=chunk.page,

                section=chunk.section,

                subsection=chunk.subsection,

                content=chunk.content,

                character_count=chunk.character_count,

                embedding=vector

            )

        )

    return embedded_chunks