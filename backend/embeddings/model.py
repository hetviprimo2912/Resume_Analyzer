from sentence_transformers import SentenceTransformer


# --------------------------------------------------
# Singleton embedding model
# --------------------------------------------------

_embedding_model = None


def get_embedding_model() -> SentenceTransformer:
    """
    Load the embedding model only once.

    Returns:
        SentenceTransformer instance.
    """

    global _embedding_model

    if _embedding_model is None:

        print("Loading embedding model...")

        _embedding_model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

        print("Embedding model loaded.")

    return _embedding_model