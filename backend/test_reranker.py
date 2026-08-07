from services.resume_search import search_resume
from retrieval.reranker import rerank


def main():

    resume_id = "40559572-4ba5-4539-b043-7042b7e50e54"

    question = "What machine learning projects has the candidate built?"

    # -----------------------------
    # Retrieve Top 10 from FAISS
    # -----------------------------
    results = search_resume(
        resume_id=resume_id,
        query=question,
        top_k=10
    )

    print("\n")
    print("=" * 80)
    print("BEFORE RERANKING")
    print("=" * 80)

    for i, result in enumerate(results, start=1):

        chunk = result["chunk"]

        print(f"\nRank : {i}")
        print(f"Distance : {result['distance']:.4f}")
        print(f"Section : {chunk.section}")
        print(f"Subsection : {chunk.subsection}")

    # -----------------------------
    # Rerank
    # -----------------------------
    reranked = rerank(
        question,
        results
    )

    print("\n")
    print("=" * 80)
    print("AFTER RERANKING")
    print("=" * 80)

    for i, result in enumerate(reranked, start=1):

        chunk = result["chunk"]

        print(f"\nRank : {i}")
        print(f"Score : {result['rerank_score']:.4f}")
        print(f"Section : {chunk.section}")
        print(f"Subsection : {chunk.subsection}")


if __name__ == "__main__":
    main()