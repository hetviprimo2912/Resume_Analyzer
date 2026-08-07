from llm.service import generate_resume_answer


def main():

    resume_id = "40559572-4ba5-4539-b043-7042b7e50e54"

    question = "What machine learning projects has the candidate built?"

    result = generate_resume_answer(
        resume_id=resume_id,
        question=question
    )

    print("\n" + "=" * 80)
    print("AI ANSWER")
    print("=" * 80)
    print()

    print(result["answer"])
    print("\nConfidence:", result["confidence"])
    print("\n" + "=" * 80)
    print("SOURCES")
    print("=" * 80)

    for rank, item in enumerate(result["matches"], start=1):

        chunk = item["chunk"]

        print(f"\nRank       : {rank}")
        print(f"Section    : {chunk.section}")
        print(f"Subsection : {chunk.subsection}")
        print(f"Page       : {chunk.page}")
        print(f"Distance   : {item['distance']:.4f}")


if __name__ == "__main__":
    main()