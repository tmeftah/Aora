import os
import hashlib
import time
import chromadb

from pypdf import PdfReader
from sentence_transformers import SentenceTransformer

from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from models.sqlalchemy_models import Documents

# === CONFIGURATION ===
DOCUMENTS_FOLDER = "documents/"
CACHE_FILE = "document_cache.json"
TOPIC_FILE = "document_topics.json"

# Initialize ChromaDB
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="documents")
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

DATABASE_URL = os.getenv("DATABASE_URL", "aora.db")
engine = create_engine("sqlite:///"+DATABASE_URL)
Base = declarative_base()


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def check_file_in_db(file_name):
    return session.query(Documents).filter(Documents.filename == file_name).first()


def compute_document_hash(text):
    """Compute SHA256 hash of document text to track changes."""
    return hashlib.sha256(text.encode()).hexdigest()


def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    reader = PdfReader(pdf_path)
    return "\n".join(
        [page.extract_text() for page in reader.pages if page.extract_text()]
    ).strip()


def chunk_text(text, chunk_size=500):
    """Split text into smaller chunks for efficient vector storage."""
    words = text.split()
    return [
        " ".join(words[i: i + chunk_size])
        for i in range(0, len(words), chunk_size)
    ]


def get_embedding(text):
    """Generate embeddings using SentenceTransformers."""
    return embedding_model.encode(text).tolist()


def update_document_in_db(document_name: str, doc_hash):
    document = session.query(Documents).filter(
        Documents.filename == document_name).first()
    if not document:
        return "Document not found"
    document.filehash = doc_hash
    document.vectorized = True
    session.commit()


def process_document(pdf_path, document):
    """Extract, chunk, and store embeddings for a PDF under a specific topic."""

    text = extract_text_from_pdf(pdf_path)
    doc_hash = compute_document_hash(text)
    document_name = document.filename
    topic = document.topic.name

    if document.filehash == doc_hash:
        print(f"✅ {pdf_path} is unchanged. Skipping re-processing...")
        update_document_in_db(document_name, doc_hash)
        return

    # Remove old embeddings before re-indexing
    collection.delete(where={"document_id": pdf_path})

    print(f"🔄 Processing {pdf_path} under topic '{topic}'...")
    chunks = chunk_text(text)

    for i, chunk in enumerate(chunks):
        embedding = get_embedding(chunk)
        collection.add(
            ids=[f"{pdf_path}_{i}"],
            documents=[chunk],
            embeddings=[embedding],
            metadatas=[{"document_id": pdf_path, "topic": topic}]),

    update_document_in_db(document_name, doc_hash)

    print(
        f"✅ Indexed {len(chunks)} chunks from {pdf_path} under topic: {topic}"
    )


def get_not_vectorized_docs():
    return session.query(Documents).filter(Documents.vectorized == False).all()


def monitor_folder():
    """Continuously monitor the document folder for changes."""

    while True:
        print("\n🔍 Checking for new, updated, or deleted documents...")

        check_docs = get_not_vectorized_docs()
        for file_name in os.listdir(DOCUMENTS_FOLDER):
            if file_name.endswith(".pdf"):

                file_exists = check_file_in_db(file_name)
                if not file_exists:
                    return "No Such file exists in directory"

                file_path = os.path.join(
                    DOCUMENTS_FOLDER, file_exists.filename)
                process_document(
                    file_path, file_exists)

        print("✅ Vectorization complete. Checking again in 60 seconds...")
        time.sleep(60)


if __name__ == '__main__':
    monitor_folder()
