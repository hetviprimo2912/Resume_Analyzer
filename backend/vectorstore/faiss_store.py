import faiss
import pickle
import numpy as np

from pathlib import Path

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

        for distance, index in zip(
            distances[0],
            indices[0]
        ):

            if index == -1:
                continue

            results.append(
                {
                    "distance": float(distance),
                    "chunk": self.metadata[index]
                }
            )

        return results
    
    def save(self, directory: str):
        """
        Save the FAISS index and metadata.
        """

        directory = Path(directory)

        directory.mkdir(
            parents=True,
            exist_ok=True
        )

        faiss.write_index(
            self.index,
            str(directory / "index.faiss")
        )

        with open(
            directory / "metadata.pkl",
            "wb"
        ) as file:

            pickle.dump(
                self.metadata,
                file
            )
            
    @classmethod
    def load(cls, directory: str):
        """
        Load a FAISS index and its metadata.
        """

        directory = Path(directory)

        index = faiss.read_index(
            str(directory / "index.faiss")
        )

        with open(
            directory / "metadata.pkl",
            "rb"
        ) as file:

            metadata = pickle.load(file)

        store = cls(index.d)

        store.index = index

        store.metadata = metadata

        return store