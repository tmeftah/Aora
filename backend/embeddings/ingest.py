# LangChain supports many other chat models. Here, we're using Ollama
# from langchain_community.chat_models import ChatOllama
# from langchain_core.output_parsers import StrOutputParser
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.runnables import RunnablePassthrough
# from langchain_core.documents import Document

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_chroma import Chroma
from langchain_community.embeddings import OllamaEmbeddings
import os
import argparse

import chromadb

parser = argparse.ArgumentParser(description="Averroes - Chatbot")
parser.add_argument("indexing", type=int, help="indexing")


def create_vectorstore():
    text_splitter = RecursiveCharacterTextSplitter(
        # Set a really small chunk size, just to show.
        chunk_size=1300,
        chunk_overlap=110,
        length_function=len,
    )

    documents = []
    for file in os.listdir("docs"):
        if file.endswith(".pdf"):
            pdf_path = "./docs/" + file
            loader = PyPDFLoader(pdf_path)
            doc = loader.load()
            document_split = text_splitter.split_documents(doc)
            documents.extend(document_split)

    Chroma.from_documents(
        collection_name="kardex",
        documents=documents,
        embedding=OllamaEmbeddings(model="mxbai-embed-large"),
        persist_directory="./vectorstore/chroma_db",
    )

    print("vectorstore created...")


def get_vectorstore():
    persistent_client = chromadb.PersistentClient(path="./vectorstore/chroma_db")
    langchain_chroma = Chroma(
        client=persistent_client,
        collection_name="kardex",
        embedding_function=OllamaEmbeddings(model="mxbai-embed-large"),
    )
    # print("There are", langchain_chroma._collection.count(), "in the collection")
    # print("There are", langchain_chroma.similarity_search("bmw?"))
    return langchain_chroma.as_retriever(
        search_type="mmr", search_kwargs={"k": 3, "lambda_mult": 0.25}
    )


if __name__ == "__main__":
    # create_vectorstore()
    store = get_vectorstore()
    docs = store.invoke(" Wearable Task Assistant?")
    print(docs)
