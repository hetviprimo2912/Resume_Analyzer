from embeddings.model import get_embedding_model


def main():

    model = get_embedding_model()

    print()

    print("Model Loaded Successfully!")

    print(model)


if __name__ == "__main__":
    main()