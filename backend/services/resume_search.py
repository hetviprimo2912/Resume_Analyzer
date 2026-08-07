from pathlib import Path
from retrieval.intent_router import (
    detect_section,
    ResumeSection
)
from retrieval.reranker import rerank
from vectorstore.faiss_store import FAISSStore

def search_resume(
    resume_id: str,
    query: str,
    top_k: int = 3
):
    """
    Search an indexed resume.
    """

    store_path = Path("storage") / resume_id

    if not store_path.exists():

        raise FileNotFoundError(
            f"Resume '{resume_id}' not found."
        )

    store = FAISSStore.load(
        str(store_path)
    )

    # ----------------------------
    # Detect query intent
    # ----------------------------
    section = detect_section(query)

    # ----------------------------
    # Get more candidates from FAISS
    # ----------------------------
    results = store.search(
        query=query,
        top_k=30
    )

    results = rerank(
        question=query,
        results=results
    )

    results = results[:5]
    print("\n========== RAW FAISS RESULTS ==========")
    print("Total Results:", len(results))

    for i, result in enumerate(results):

        chunk = result["chunk"]

        print("--------------------------------")
        print("Result:", i + 1)
        print("Distance:", result["distance"])
        print("Section:", chunk.section)
        print("Subsection:", chunk.subsection)
        print("Content:")
        print(chunk.content[:200])
    # ----------------------------
    # Re-rank results
    # ----------------------------
    results = rerank(
        question=query,
        results=results
    )
    print("\n========== RERANKED RESULTS ==========")

    for result in results:

        print("--------------------------------")
        print(result["rerank_score"])
        print(result["chunk"].section)
        print(result["chunk"].subsection)
    # ----------------------------
    # Remove weak matches
    # ----------------------------
    # results = [
    #     result
    #     for result in results
    #     if result["rerank_score"] > 4
    # ]
    # ----------------------------
    # Remove duplicate chunks
    # ----------------------------
    unique_results = []

    seen = set()

    for result in results:

        chunk = result["chunk"]

        key = (
            chunk.section,
            chunk.subsection
        )

        if key in seen:
            continue

        seen.add(key)

        unique_results.append(result)

    results = unique_results
    # ----------------------------
    # General query?
    # ----------------------------
    if section == ResumeSection.GENERAL:
        return results[:top_k]

    # ----------------------------
    # Filter by section
    # ----------------------------
    filtered = []

    for result in results:

        chunk = result["chunk"]

        chunk_section = (
            chunk.section
            .replace(" ", "")
            .upper()
        )

        if chunk_section == section.value:

            filtered.append(result)

    # ----------------------------
    # Fallback
    # ----------------------------
    if filtered:

        return filtered[:top_k]

    return results[:top_k]