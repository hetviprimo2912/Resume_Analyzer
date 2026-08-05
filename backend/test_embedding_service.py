from embeddings.service import embed_text


def main():

    text = """
    Python
    React
    Node.js
    Machine Learning
    """

    embedding = embed_text(text)

    print(f"Embedding Dimension : {len(embedding)}")
    print()
    print("First 10 Values:")
    print(embedding[:10])


if __name__ == "__main__":
    main()