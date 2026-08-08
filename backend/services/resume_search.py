from pathlib import Path
from retrieval.intent_router import (
    detect_section,
    ResumeSection
)
from retrieval.reranker import rerank
from vectorstore.faiss_store import FAISSStore

def is_identity_chunk(chunk):
    """
    Detect whether a chunk likely represents
    the candidate's name / identity header.
    """

    section = (
        chunk.section
        .replace(" ", "")
        .strip()
    )

    if not section:
        return False

    normalized = section.upper()

    known_sections = {
        "PROJECTS",
        "PROJECT",
        "SKILLS",
        "SKILL",
        "EDUCATION",
        "CONTACT",
        "ABOUT",
        "ABOUTME",
        "EXPERIENCE",
        "SUMMARY",
        "PROFILE",
    }

    if normalized in known_sections:
        return False

    # Candidate name headers are generally short.
    if len(normalized) > 40:
        return False

    # Ignore strings containing numbers.
    if any(char.isdigit() for char in normalized):
        return False

    # Ignore obvious sentence-like headers.
    if len(normalized.split()) > 6:
        return False

    return True

# def search_resume(
#     resume_id: str,
#     query: str,
#     top_k: int = 3
# ):
#     """
#     Search an indexed resume.
#     """

#     store_path = Path("storage") / resume_id

#     if not store_path.exists():

#         raise FileNotFoundError(
#             f"Resume '{resume_id}' not found."
#         )

#     store = FAISSStore.load(
#         str(store_path)
#     )

#     # ----------------------------
#     # Detect query intent
#     # ----------------------------
#     section = detect_section(query)

#     # ----------------------------
#     # Get more candidates from FAISS
#     # ----------------------------
#     results = store.search(
#         query=query,
#         top_k=30
#     )

#     results = rerank(
#         question=query,
#         results=results
#     )

#     results = results[:5]
#     print("\n========== RAW FAISS RESULTS ==========")
#     print("Total Results:", len(results))

#     for i, result in enumerate(results):

#         chunk = result["chunk"]

#         print("--------------------------------")
#         print("Result:", i + 1)
#         print("Distance:", result["distance"])
#         print("Section:", chunk.section)
#         print("Subsection:", chunk.subsection)
#         print("Content:")
#         print(chunk.content[:200])
#     # ----------------------------
#     # Re-rank results
#     # ----------------------------
#     results = rerank(
#         question=query,
#         results=results
#     )
#     print("\n========== RERANKED RESULTS ==========")

#     for result in results:

#         print("--------------------------------")
#         print(result["rerank_score"])
#         print(result["chunk"].section)
#         print(result["chunk"].subsection)
#     # ----------------------------
#     # Remove weak matches
#     # ----------------------------
#     # results = [
#     #     result
#     #     for result in results
#     #     if result["rerank_score"] > 4
#     # ]
#     # ----------------------------
#     # Remove duplicate chunks
#     # ----------------------------
#     unique_results = []

#     seen = set()

#     for result in results:

#         chunk = result["chunk"]

#         key = (
#             chunk.section,
#             chunk.subsection
#         )

#         if key in seen:
#             continue

#         seen.add(key)

#         unique_results.append(result)

#     results = unique_results
#     # ----------------------------
#     # General query
#     # ----------------------------

#     if section == ResumeSection.GENERAL:

#         return results[:top_k]


#     # ----------------------------
#     # Identity / Name query
#     # ----------------------------

#     if section == ResumeSection.IDENTITY:
        
#         # ----------------------------
#         # Contact field queries
#         # ----------------------------

#         contact_sections = {
#             ResumeSection.EMAIL,
#             ResumeSection.PHONE,
#             ResumeSection.LINKEDIN,
#             ResumeSection.GITHUB,
#             ResumeSection.ADDRESS,
#             ResumeSection.CONTACT,
#         }

#         if section in contact_sections:

#             contact_results = []

#             for result in results:

#                 chunk = result["chunk"]

#                 chunk_section = (
#                     chunk.section
#                     .replace(" ", "")
#                     .upper()
#                 )

#                 if chunk_section == "CONTACT":

#                     contact_results.append(result)

#             if contact_results:

#                 return contact_results[:top_k]

#         identity_results = []

#         for result in results:

#             chunk = result["chunk"]

#             chunk_section = (
#                 chunk.section
#                 .replace(" ", "")
#                 .upper()
#             )

#             # The current parser may identify the candidate's
#             # name as its own section/header.
#             #
#             # We therefore look for a short header that is
#             # not one of the known resume sections.

#             known_sections = {
#                 "PROJECTS",
#                 "SKILLS",
#                 "EDUCATION",
#                 "CONTACT",
#                 "ABOUTME",
#                 "ABOUT",
#                 "EXPERIENCE",
#                 "SUMMARY",
#                 "PROFILE",
#             }

#             # if (
#             #     chunk_section
#             #     and chunk_section not in known_sections
#             #     and len(chunk_section) <= 40
#             # ):
#             #     identity_results.append(result)
#             if is_identity_chunk(chunk):

#                 identity_results.append(result)

#         if identity_results:

#             return identity_results[:top_k]


#     # ----------------------------
#     # Section-based filtering
#     # ----------------------------

#     filtered = []

#     for result in results:

#         chunk = result["chunk"]

#         chunk_section = (
#             chunk.section
#             .replace(" ", "")
#             .upper()
#         )

#         # Normalize common section names.
#         section_aliases = {

#             "ABOUTME": "ABOUT",

#             "ABOUT": "ABOUT",

#             "S K I L L S": "SKILLS",

#             "S K I L L": "SKILLS",

#             "PROJECT": "PROJECTS",

#             "PROJECTS": "PROJECTS",

#             "EDUCATION": "EDUCATION",

#             "E D U C A T I O N": "EDUCATION",

#             "CONTACT": "CONTACT",

#         }

#         normalized_chunk_section = section_aliases.get(
#             chunk_section,
#             chunk_section
#         )

#         if normalized_chunk_section == section.value:

#             filtered.append(result)


#     # ----------------------------
#     # Return section-specific results
#     # ----------------------------

#     if filtered:

#         return filtered[:top_k]


#     # ----------------------------
#     # Fallback
#     # ----------------------------

#     return results[:top_k]

def search_resume(
    resume_id: str,
    query: str,
    top_k: int = 3
):
    """
    Search an indexed resume using:

    1. FAISS semantic retrieval
    2. Intent detection
    3. CrossEncoder reranking
    4. Section filtering
    5. Duplicate removal
    """

    store_path = Path("storage") / resume_id

    if not store_path.exists():

        raise FileNotFoundError(
            f"Resume '{resume_id}' not found."
        )

    store = FAISSStore.load(
        str(store_path)
    )

    # =========================================================
    # STEP 1
    # Get a large candidate pool from FAISS
    # =========================================================

    results = store.search(
        query=query,
        top_k=30
    )

    print("\n========== RAW FAISS RESULTS ==========")
    print("Total Results:", len(results))

    for i, result in enumerate(results, 1):

        chunk = result["chunk"]

        print("--------------------------------")
        print("Result:", i)
        print("Distance:", result["distance"])
        print("Section:", chunk.section)
        print("Subsection:", chunk.subsection)
        print("Content:")
        print(chunk.content[:200])

    # =========================================================
    # STEP 2
    # Detect query intent
    #
    # IMPORTANT:
    # Pass chunks so the router can recognize project names.
    # =========================================================

    section = detect_section(
        query=query,
        chunks=[
            result["chunk"]
            for result in results
        ]
    )

    print("\n========== DETECTED SECTION ==========")
    print("Query:", query)
    print("Section:", section.value)

    # =========================================================
    # STEP 3
    # Rerank ALL FAISS candidates
    #
    # IMPORTANT:
    # Do NOT do results[:5] here.
    # =========================================================

    results = rerank(
        question=query,
        results=results
    )

    print("\n========== RERANKED RESULTS ==========")

    for result in results:

        print("--------------------------------")
        print(
            "Score:",
            result["rerank_score"]
        )
        print(
            "Section:",
            result["chunk"].section
        )
        print(
            "Subsection:",
            result["chunk"].subsection
        )

    # =========================================================
    # STEP 4
    # Remove duplicate chunks
    # =========================================================

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

    # =========================================================
    # STEP 5
    # Candidate name
    # =========================================================

    if section == ResumeSection.IDENTITY:

        identity_results = []

        for result in results:

            chunk = result["chunk"]

            if is_identity_chunk(chunk):

                identity_results.append(result)

        print(
            "\n========== IDENTITY RESULTS =========="
        )

        for result in identity_results[:top_k]:

            print(
                result["chunk"].section,
                "|",
                result["rerank_score"]
            )

        if identity_results:

            return identity_results[:top_k]

    # =========================================================
    # STEP 6
    # Contact-specific fields
    #
    # EMAIL / PHONE / LINKEDIN / GITHUB / ADDRESS
    # all live inside the CONTACT chunk.
    # =========================================================

    contact_sections = {
        ResumeSection.EMAIL,
        ResumeSection.PHONE,
        ResumeSection.LINKEDIN,
        ResumeSection.GITHUB,
        ResumeSection.ADDRESS,
        ResumeSection.CONTACT,
    }

    if section in contact_sections:

        contact_results = []

        for result in results:

            chunk = result["chunk"]

            chunk_section = (
                chunk.section
                .replace(" ", "")
                .upper()
            )

            if chunk_section == "CONTACT":

                contact_results.append(result)

        print(
            "\n========== CONTACT RESULTS =========="
        )

        for result in contact_results[:top_k]:

            print(
                result["chunk"].section,
                "|",
                result["chunk"].subsection,
                "|",
                result["rerank_score"]
            )

        if contact_results:

            return contact_results[:top_k]

        # If no CONTACT chunk was retrieved,
        # don't immediately return unrelated results.
        return []

    # =========================================================
    # STEP 7
    # General query
    # =========================================================

    if section == ResumeSection.GENERAL:

        return results[:top_k]

    # =========================================================
    # STEP 8
    # Section-based filtering
    # =========================================================

    filtered = []

    for result in results:

        chunk = result["chunk"]

        chunk_section = (
            chunk.section
            .replace(" ", "")
            .upper()
        )

        # Normalize section names.
        section_aliases = {

            "ABOUTME": "ABOUT",
            "ABOUT": "ABOUT",

            "SKILL": "SKILLS",
            "SKILLS": "SKILLS",

            "PROJECT": "PROJECTS",
            "PROJECTS": "PROJECTS",

            "EDUCATION": "EDUCATION",

            "CONTACT": "CONTACT",
        }

        normalized_chunk_section = (
            section_aliases.get(
                chunk_section,
                chunk_section
            )
        )

        if (
            normalized_chunk_section
            == section.value
        ):

            filtered.append(result)

    print(
        "\n========== SECTION FILTERED RESULTS =========="
    )
    print(
        "Requested section:",
        section.value
    )
    print(
        "Matching chunks:",
        len(filtered)
    )

    for result in filtered[:top_k]:

        print(
            result["chunk"].section,
            "|",
            result["chunk"].subsection,
            "|",
            result["rerank_score"]
        )

    # =========================================================
    # STEP 9
    # Return section-specific results
    # =========================================================

    if filtered:

        return filtered[:top_k]

    # =========================================================
    # STEP 10
    # No relevant section found
    #
    # IMPORTANT:
    # For a specific intent, don't feed unrelated sections
    # to the LLM.
    # =========================================================

    return []