import os
import json
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import ollama

from backend.exceptions import ModelsNotRetrievedException

TEMPLATE = """You are an AI assistant and based on the context provided below, please provide a brief answer starting with 'Based on the given context'. Do not use external knowledge or make assumptions beyond the context
context and nothing else. If you do not know the answer please strictly say "I couldn't find the answer to that question. Please contact our support team for more assistance."
Question: {input}
Context: {context}
"""


def get_list_available_models():
  
    """List all downloaded ollama models"""

    try:
        client =  ollama.Client(host=os.getenv("OLLAMA_API_URL"))
        
      
        return  [model['name'] for model in client.list()['models']]
        
    except Exception as e:         
        raise ModelsNotRetrievedException()


def get_chat_model(model_name: str="llama3"):
    """
    Return an instance of ChatOllama based on the given model_name.
    """
   
    try:
        if model_name in  get_list_available_models():
            return ChatOllama(model=model_name, temperature=0.7)
        raise ValueError(f"Unsupported model name: {model_name}")
    
    #TODO Better Exception
    except Exception as e:
        raise ValueError(f"Unsupported model name: {model_name}")


def create_chain(model_name: str):
    """
    Create the chain with the dynamic model.
    """

    chat_model = get_chat_model(model_name)
    prompt = ChatPromptTemplate.from_template(TEMPLATE)
    chain = prompt | chat_model | StrOutputParser()

    return chain
