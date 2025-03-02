import json
import requests
import os
from backend.exceptions import ModelsNotRetrievedException
from backend.service.llm_utils import get_list_available_models


async def query_service(query: str, model_name: str):
    """
    Process a query and return a streaming response.
    """

    try:

        api_key = os.getenv("GROQ_API_KEY")
        api_key = "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"

        if not api_key:
            raise ValueError(
                "API key is missing. Please set the GROQ_API_KEY environment variable.")

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        url = "https://api.groq.com/openai/v1/chat/completions"

        data = {
            "messages": [{"role": "user", "content": query}],
            "model": model_name,
            "temperature": 1,
            "max_completion_tokens": 1024,
            "top_p": 1,
            "stream": False,
            # "response_format": {"type": "json_object"},
            "stop": None
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        response_json = response.json()
        return response_json.get('choices', [{}])[0].get('message', {}).get('content', "No content returned.")

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
        # return get_list_available_models()
        api_key = os.getenv("GROQ_API_KEY")
        api_key = "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"
        if not api_key:
            raise ValueError(
                "API key is missing. Please set the GROQ_API_KEY environment variable.")

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        url = "https://api.groq.com/openai/v1/models"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            model_names = [model["id"] for model in data.get("data", [])]
            return model_names
        else:
            print(
                f"Failed to fetch models: {response.status_code}, {response.text}")
            return []

    except Exception as e:
        raise ModelsNotRetrievedException()
