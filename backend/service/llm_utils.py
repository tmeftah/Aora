from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

TEMPLATE = """<|begin_of_text|><|start_header_id|>system<|end_header_id|>
You are an AI assistant, you only answer questions on the folwing
context and nothing else. If you do not know the answer please strictly say
'see Documentation'<|eot_id|><|start_header_id|>user<|end_header_id|>
Question: {input}
Context: {context}
<|eot_id|><|start_header_id|>assistant<|end_header_id|>"""


def get_chat_model(model_name: str):
    """
    Return an instance of ChatOllama based on the given model_name.
    """
    if model_name == "llama3":
        return ChatOllama(model="llama3", temperature=0.5)
    elif model_name == "other_model":
        return ChatOllama(model="other_model", temperature=0.7)
    else:
        raise ValueError(f"Unsupported model name: {model_name}")


def create_chain(model_name: str):
    """
    Create the chain with the dynamic model.
    """

    chat_model = get_chat_model(model_name)
    prompt = ChatPromptTemplate.from_template(TEMPLATE)
    chain = prompt | chat_model | StrOutputParser()

    return chain
