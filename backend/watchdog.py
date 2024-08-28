import os
import sys
import time
import hashlib
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base


from sqlalchemy.orm import sessionmaker
from datetime import datetime
from models.sqlalchemy_models import Documents


from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
import chromadb


from dotenv import load_dotenv

load_dotenv()
directory = './docs'

# Get the path value from .env file
relative_path = os.getenv("DATABASE_PATH").replace(".","")
# Get directory of script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Append the relative path to the script directory
persist_directory = os.path.join(script_dir, ("."+relative_path))

print(persist_directory)


DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///aora.db")
engine = create_engine(DATABASE_URL)
Base = declarative_base()





Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

def check_file_in_db(filename):
    return session.query(Documents).filter_by(filename=filename).first()

def update_file_status(filename):
    file = check_file_in_db(filename)
    file_hash = hashlib.sha256(open(os.path.join(directory, filename), "rb").read()).hexdigest()

    if file and file.status != "done":
      
        file.status = "uploaded"
        file.updated_at = datetime.now()
        session.commit()        
        create_vectorstore(filename)

        file.status = "done"
        file.updated_at = datetime.now()
        session.commit()   
    

def create_vectorstore(filename):
    text_splitter = RecursiveCharacterTextSplitter(
        # Set a really small chunk size, just to show.
        chunk_size=1300,
        chunk_overlap=110,
        length_function=len,
    )

 
    loader = PyPDFLoader(os.path.join(directory, filename))
    doc = loader.load()
    document_split = text_splitter.split_documents(doc)

    Chroma.from_documents(
        collection_name=os.environ.get("COLLECTION_NAME"),
        documents=document_split,
        embedding=OllamaEmbeddings(model="mxbai-embed-large"),
        persist_directory=persist_directory,
        collection_metadata={"hnsw:space": "cosine"}
    )

    print("vectorstore created...")

def monitor_directory(directory):
    previous_files = set()
    while True:
        try:
            current_files = set(os.listdir(directory))
            print("current_files:", current_files)
            new_files = current_files - previous_files
            for filename in new_files:
                file_path = os.path.join(directory, filename)
                if os.path.isfile(file_path):
                    update_file_status(filename)
            previous_files = current_files
            print(50* "*")
            time.sleep(3)
        except KeyboardInterrupt:
            print('Stopping script...')
            session.close()
            sys.exit(0)
       

def main():
    
    monitor_directory(directory)

if __name__ == '__main__':
    main()