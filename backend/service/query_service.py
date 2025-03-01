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
            "model": "llama-3.3-70b-versatile",
            "temperature": 1,
            "max_completion_tokens": 1024,
            "top_p": 1,
            "stream": False,
            # "response_format": {"type": "json_object"},
            "stop": None
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))
        print(response)
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
        return ['llama-3.3-70b-versatile']

    except Exception as e:
        raise ModelsNotRetrievedException()
