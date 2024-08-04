# LangChain supports many other chat models. Here, we're using Ollama
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_chroma import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_core.documents import Document
import os
import argparse

parser = argparse.ArgumentParser(description="Averroes - Chatbot")
parser.add_argument("indexing", type=int, help="indexing")


def create_vectorstore():

    documents = []
    for file in os.listdir('docs'):
        if file.endswith('.pdf'):
            pdf_path = './docs/' + file
            loader = PyPDFLoader(pdf_path)
            documents.extend(loader.load())

    text_splitter = RecursiveCharacterTextSplitter(
        # Set a really small chunk size, just to show.
        chunk_size=1300,
        chunk_overlap=200,
        length_function=len
    )
    documents = text_splitter.split_documents(documents)

    print(len(documents))
    # print(documents)
    vectorstore = Chroma.from_documents(
        documents,
        embedding=OllamaEmbeddings(model="mxbai-embed-large"),
    )

    return vectorstore


def create_llm(llm_name: str = "llama3", vectorstore=None):

    # supports many more optional parameters. Hover on your `ChatOllama(...)`
    # class to view the latest available supported parameters
    llm = ChatOllama(model=llm_name)

    message = """
    Answer this question using the provided context only. Write on your own style.

    {question}

    Context:
    {context}
    """

    # using LangChain Expressive Language chain syntax
    # learn more about the LCEL on
    # /docs/concepts/#langchain-expression-language-lcel
    prompt = ChatPromptTemplate.from_messages([("human", message)])

    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4},
    )

    chain = {"context": retriever, "question": RunnablePassthrough()
             } | prompt | llm | StrOutputParser()

    return chain

# for brevity, response is printed in terminal
# You can use LangServe to deploy your application for
# production


def resp(message, history):
    store = create_vectorstore()
    chain = create_llm(llm_name="llama3", vectorstore=store)
    yield chain.invoke({"question": message})


if __name__ == "__main__":
    import gradio as gr

    gr.ChatInterface(resp,
                     title="K-Averroes", examples=["what do we need for a request?",
                                                   "which .NET version is used with Power Pick System?",
                                                   "what can we do with WTA?",
                                                   "since when we can use gpx?"
                                                   ]).launch()
