# THIS IS DEPRICATED SCRIPT, WHICH IS NO LONGER USED
# PLEASE USE create_embeddings.py FILE
import hashlib
import json
import os
import time

import chromadb
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer


# === CONFIGURATION ===
DOCUMENTS_FOLDER = "documents/"
CACHE_FILE = "document_cache.json"
TOPIC_FILE = "document_topics.json"

# Initialize ChromaDB
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="documents")
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# === HELPER FUNCTIONS ===


def load_json(file_path):
    """Load JSON data from a file."""
    if os.path.exists(file_path):
        with open(file_path) as file:

            return json.load(file)
    return {}


def save_json(file_path, data):
    """Save JSON data to a file."""
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)


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


def process_document(pdf_path, topic):
    """Extract, chunk, and store embeddings for a PDF under a specific topic."""
    text = extract_text_from_pdf(pdf_path)
    doc_hash = compute_document_hash(text)

    # Load existing topics & cache
    topics = load_json(TOPIC_FILE)
    document_cache = load_json(CACHE_FILE)

    # Store document topic
    topics[pdf_path] = topic
    save_json(TOPIC_FILE, topics)

    # Check if the document is already indexed and unchanged
    if pdf_path in document_cache and document_cache[pdf_path] == doc_hash:
        print(f"✅ {pdf_path} is unchanged. Skipping re-processing...")
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

    # Update cache with new document hash
    document_cache[pdf_path] = doc_hash
    save_json(CACHE_FILE, document_cache)

    print(
        f"✅ Indexed {len(chunks)} chunks from {pdf_path} under topic: {topic}"
    )


def remove_deleted_files():
    """Check for deleted files and remove their embeddings from ChromaDB."""
    document_cache = load_json(CACHE_FILE)
    topics = load_json(TOPIC_FILE)

    existing_files = set(os.listdir(DOCUMENTS_FOLDER))
    deleted_files = [
        file for file in document_cache.keys() if file not in existing_files
    ]

    for deleted_file in deleted_files:
        print(f"🗑️ Removing deleted document: {deleted_file} from ChromaDB...")
        collection.delete(where={"document_id": deleted_file})
        document_cache.pop(deleted_file, None)
        topics.pop(deleted_file, None)

    save_json(CACHE_FILE, document_cache)
    save_json(TOPIC_FILE, topics)


def monitor_folder():
    """Continuously monitor the document folder for changes."""
    while True:
        print("\n🔍 THIS IS A OLD SCRIPT, DO NOT RUN. \
                PLEASE USE create_embeddings.py FILE \
              TO CREATE YOUR EMBEDDINGS")
        print("\n🔍 Checking for new, updated, or deleted documents...")

        for file_name in os.listdir(DOCUMENTS_FOLDER):
            if file_name.endswith(".pdf"):
                file_path = os.path.join(DOCUMENTS_FOLDER, file_name)
                # Ask user to set topic
                topic = input(f"📌 Enter topic for {file_name}: ")
                # process_document(file_path, topic)
                pass

        print("✅ Vectorization complete. Checking again in 60 seconds...")
        time.sleep(60)


if __name__ == "__main__":
    monitor_folder()
