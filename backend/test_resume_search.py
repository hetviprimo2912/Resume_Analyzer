from services.resume_search import search_resume

resume_id = input("Resume ID: ")

query = input("Question: ")

results = search_resume(
    resume_id=resume_id,
    query=query,
    top_k=3
)

print()

for rank, result in enumerate(results, start=1):

    chunk = result["chunk"]

    print("=" * 60)

    print("Rank:", rank)
    print("Distance:", round(result["distance"], 4))
    print("Section:", chunk.section)
    print("Subsection:", chunk.subsection)

    print()

    print(chunk.content)
    print()