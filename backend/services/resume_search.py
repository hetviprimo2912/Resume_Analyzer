from pathlib import Path
from retrieval.intent_router import (
    detect_section,
    ResumeSection
)

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
        top_k=20
    )

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