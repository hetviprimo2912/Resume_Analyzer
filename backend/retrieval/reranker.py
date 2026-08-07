from sentence_transformers import CrossEncoder

print("Loading reranker model...")

reranker = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)

print("Reranker model loaded.")


def rerank(question, results):
    """
    Re-rank FAISS search results using a CrossEncoder.
    """

    if not results:
        return []

    sentence_pairs = []

    for result in results:

        sentence_pairs.append(
            (
                question,
                result["chunk"].content
            )
        )

    scores = reranker.predict(
        sentence_pairs
    )

    reranked = []

    for score, result in zip(scores, results):

        result["rerank_score"] = float(score)

        reranked.append(result)

    reranked.sort(
        key=lambda x: x["rerank_score"],
        reverse=True
    )

    return reranked