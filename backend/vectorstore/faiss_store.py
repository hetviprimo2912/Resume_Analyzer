import faiss
import numpy as np
from embeddings.service import embed_text

class FAISSStore:
    """
    Stores resume embeddings inside a FAISS index.
    """

    def __init__(self, embedding_dimension: int):

        self.dimension = embedding_dimension

        self.index = faiss.IndexFlatL2(
            embedding_dimension
        )

        self.metadata = []
    
    def add_embeddings(self, embeddings):
        """
        Add resume embeddings into the FAISS index.
        """

        vectors = []

        for item in embeddings:

            vectors.append(item.embedding)

            self.metadata.append(item)

        vectors = np.array(
            vectors,
            dtype=np.float32
        )

        self.index.add(vectors)
        
    def search(
        self,
        query: str,
        top_k: int = 3
    ):
        """
        Search for the most similar resume chunks.
        """

        query_vector = embed_text(query)

        query_vector = np.array(
            [query_vector],
            dtype=np.float32
        )

        distances, indices = self.index.search(
            query_vector,
            top_k
        )

        results = []

        for index in indices[0]:

            if index == -1:
                continue

            results.append(
                self.metadata[index]
            )

        return results