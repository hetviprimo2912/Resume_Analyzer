from services.resume_search import search_resume

from llm.prompt_builder import build_prompt
from llm.model import generate_response

def calculate_confidence(matches):
    """
    Calculate a confidence score (0-100)
    from the best reranker score.
    """

    if not matches:
        return 0

    best_score = matches[0].get("rerank_score", 0)

    confidence = max(
        0,
        min(
            100,
            round((best_score + 15) / 15 * 100)
        )
    )

    return confidence
def generate_resume_answer(
    resume_id: str,
    question: str,
    top_k: int = 3
):
    """
    Search the resume, build a prompt,
    generate an answer using the LLM.
    """

    # -----------------------------
    # Retrieve relevant resume chunks
    # -----------------------------
    matches = search_resume(
        resume_id=resume_id,
        query=question,
        top_k=top_k
    )
    print("\n========== RETRIEVED CHUNKS ==========")

    for i, result in enumerate(matches, 1):

        chunk = result["chunk"]

        print(f"\nChunk {i}")

        print("Section:", chunk.section)

        print("Subsection:", chunk.subsection)

        print("Score:", result.get("rerank_score"))

        print(chunk.content[:300])

    print("======================================\n")
    # -----------------------------
    # Build prompt
    # -----------------------------
    prompt = build_prompt(
        question=question,
        matches=matches
    )
    print("\n========== PROMPT ==========")
    print(prompt)
    print("============================\n")
    # -----------------------------
    # Generate answer
    # -----------------------------
    answer = generate_response(
        prompt
    )
    confidence = calculate_confidence(
        matches
    )
    
    return {
        "answer": answer,
        "confidence": confidence,
        "matches": matches
    }