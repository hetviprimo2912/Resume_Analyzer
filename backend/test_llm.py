from llm.model import generate_response


def main():

    prompt = """
You are a helpful assistant.

Question:
What is Machine Learning?

Answer:
"""

    answer = generate_response(prompt)

    print("\n" + "=" * 80)
    print("LLM RESPONSE")
    print("=" * 80)
    print()
    print(answer)


if __name__ == "__main__":
    main()