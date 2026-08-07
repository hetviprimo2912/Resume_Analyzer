# import requests

# OLLAMA_URL = "http://localhost:11434/api/generate"
# MODEL_NAME = "qwen3:8b"


# def generate_response(prompt: str) -> str:
#     """
#     Generate an answer using the local Ollama model.
#     """

#     response = requests.post(
#         OLLAMA_URL,
#         json={
#             "model": MODEL_NAME,
#             "prompt": prompt,
#             "stream": False
#         },
#         timeout=300
#     )

#     response.raise_for_status()

#     data = response.json()

#     return data["response"].strip()
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5:3b"


def generate_response(prompt: str) -> str:
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False,
        },
        timeout=300,
    )

    print("\n========== OLLAMA STATUS ==========")
    print(response.status_code)
    print("========== OLLAMA BODY ==========")
    print(response.text)
    print("==================================\n")

    if response.status_code != 200:
        raise Exception(f"Ollama Error: {response.text}")

    data = response.json()

    return data["response"].strip()