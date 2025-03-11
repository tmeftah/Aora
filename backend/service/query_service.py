import json
import os
from typing import List

import chromadb
import requests
from sentence_transformers import SentenceTransformer

from backend.exceptions import ModelsNotRetrievedException
from typing import List


# === CONFIGURATION ===
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="documents")
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# === RETRIEVE DOCUMENTS BASED ON TOPIC ===


def retrieve_relevant_chunks(query: str, topics: List[str]):
    """Retrieve the top 3 relevant document chunks from ChromaDB, filtered by topics."""
    query_embedding = embedding_model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3,
        where={"topic": {"$in": topics}},  # Filter by selected topics
    )

    return (
        results["documents"][0]
        if "documents" in results and results["documents"]
        else []
    )


async def query_service(query: str, model_name: str, topics: List[str]):
    """
    Process a query and return a streaming response.
    """

    try:

        api_key = os.getenv("LLM_API_KEY")

        if not api_key:
            raise ValueError(
                "API key is missing. Please set the GROQ_API_KEY environment variable."
            )

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }
        url = os.getenv("LLM_API_BASE_URL") + "/v1/chat/completions"

        # Retrieve relevant chunks first
        relevant_chunks = retrieve_relevant_chunks(query, topics)
        if not relevant_chunks:
            return "No relevant information found in the selected topics."

        context = "\n".join(relevant_chunks)

        data = {
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful assistant. Answer the question using the provided context.",
                },
                {
                    "role": "user",
                    "content": f"Context: {context}\n\nQuestion: {query}",
                },
            ],
            "model": model_name,
            "temperature": 1,
            "max_completion_tokens": 1024,
            "top_p": 1,
            "stream": False,
            # "response_format": {"type": "json_object"},
            "stop": None,
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        response_json = response.json()
        return (
            response_json.get("choices", [{}])[0]
            .get("message", {})
            .get("content", "No content returned.")
        )

    except requests.exceptions.RequestException as e:
        return f"Request error: {e}"
    except json.JSONDecodeError:
        return "Error decoding the JSON response."
    except KeyError:
        return "Unexpected response format from the API."
    except Exception as e:
        return f"An error occurred: {e}"


async def model_list() -> list:
    """List all downloaded ollama models"""

    try:

        api_key = os.getenv("LLM_API_KEY")

        if not api_key:
            raise ValueError(
                "API key is missing. Please set the GROQ_API_KEY environment variable."
            )

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }
        url = os.getenv("LLM_API_BASE_URL") + "/v1/models"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            # print(data)

            model_names = [model["id"] for model in data.get("data", [])]
            return model_names
        else:
            print(
                f"Failed to fetch models: {response.status_code}, {response.text}")
            return []

    except Exception as e:
        raise ModelsNotRetrievedException()
