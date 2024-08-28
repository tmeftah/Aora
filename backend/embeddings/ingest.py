# LangChain supports many other chat models. Here, we're using Ollama
# from langchain_community.chat_models import ChatOllama
# from langchain_core.output_parsers import StrOutputParser
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.runnables import RunnablePassthrough
# from langchain_core.documents import Document

import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
import chromadb

vectordatastore_directory = os.getenv("VECTORSTORE_DATABASE_PATH")
documenst_directory = os.getenv("DOCUMENTS_DIRECTORY")



def create_vectorstore():
    text_splitter = RecursiveCharacterTextSplitter(
        # Set a really small chunk size, just to show.
        chunk_size=1500,
        chunk_overlap=120,
        length_function=len,
    )

    documents = []
    for file in os.listdir(documenst_directory):
        if file.endswith(".pdf"):
            pdf_path = "./docs/" + file
            loader = PyPDFLoader(pdf_path)
            doc = loader.load()
            document_split = text_splitter.split_documents(doc)
            documents.extend(document_split)

    Chroma.from_documents(
        collection_name=os.environ.get("COLLECTION_NAME"),
        documents=documents,
        embedding=OllamaEmbeddings(model="mxbai-embed-large"),
        persist_directory=vectordatastore_directory,
    )

    print("vectorstore created...")


def get_vectorstore():
    persistent_client = chromadb.PersistentClient(path=vectordatastore_directory)

    langchain_chroma = Chroma(
        client=persistent_client,
        collection_name=os.environ.get("COLLECTION_NAME"),
        embedding_function=OllamaEmbeddings(model="mxbai-embed-large"),
        collection_metadata={"hnsw:space": "cosine"}
    )
    print("There are", langchain_chroma._collection.count(), "in the collection")

    # print("There are", langchain_chroma.similarity_search("bmw?"))
    return langchain_chroma.as_retriever(search_type="similarity_score_threshold", search_kwargs={"score_threshold": 0.2,"k":3}
    )


if __name__ == "__main__":
    # create_vectorstore()
    store = get_vectorstore()
    docs = store.invoke(" Wearable Task Assistant?")
    print(docs)
