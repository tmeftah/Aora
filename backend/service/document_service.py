import hashlib
import os
from typing import List

from fastapi import File
from sqlalchemy.orm import Session

from backend.exceptions import NoDocumentsFoundException
from backend.models.pydantic_models import DocumentPydantic
from backend.models.sqlalchemy_models import Documents
from backend.service.topics_service import get_topic_by_name

documents_directory = os.getenv("DOCUMENTS_DIRECTORY", "documents/")


def save_document(
    topic_name: str, file: File, db: Session
) -> DocumentPydantic:
    """Gets the uploaded document, saves the document
    in the docs folder and creates a hash of the document
    and saves it in db"""

    # file_directory = "docs"
    os.makedirs(documents_directory, exist_ok=True)

    file_location = os.path.join(documents_directory, file.filename)
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())

    file_hash = hashlib.sha256(open(file_location, "rb").read()).hexdigest()

    topic = get_topic_by_name(name=topic_name, db=db)
    if not topic:
        raise Exception("Topic not found")

    new_document = Documents(
        filename=file.filename,
        filehash=file_hash,
        status="on progress",
        content_type=file.content_type,
        topic_id=topic.id,
    )
    db.add(new_document)
    db.commit()

    return DocumentPydantic.model_validate(new_document)


def get_document_by_name(name: str, db: Session):
    """Get Topic by name"""

    document = db.query(Documents).filter(Documents.filename == name).first()
    return document if document else None


def delete_document(db: Session, document_name: str) -> dict:
    """Delete Topic based on user id"""

    try:
        document = get_document_by_name(name=document_name, db=db)
        if not document:
            raise NoDocumentsFoundException()

        file_path = os.path.join(documents_directory, document.filename)

        if os.path.exists(file_path):
            os.remove(file_path)

        db.delete(document)
        db.commit()
        return {"message": "Document deleted"}
    except Exception as e:
        raise e


def get_all_documents(db: Session) -> List[DocumentPydantic]:
    """Get all documents"""
    documents = db.query(Documents).all()

    return documents if documents else None


def document_list(db: Session) -> List[DocumentPydantic]:
    """Get all documents from db if there exists none,
    raise relevant exceptions"""

    documents = get_all_documents(db)
    if not documents:
        raise NoDocumentsFoundException()

    return [DocumentPydantic.model_validate(doc) for doc in documents]
