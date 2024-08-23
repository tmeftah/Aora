import hashlib
import os
from typing import List

from fastapi import File
from sqlalchemy.orm import Session

from backend.exceptions import NoDocumentsFoundException
from backend.exceptions import NoValidPermissionsException
from backend.models.pydantic_models import DocumentPydantic
from backend.models.sqlalchemy_models import Documents


def save_document(current_user, file: File, db: Session) -> DocumentPydantic:
    """Gets the uploaded document, saves the document
    in the docs folder and creates a hash of the document
    and saves it in db"""

    if current_user.role < 5:
        raise NoValidPermissionsException()

    file_directory = "docs"
    os.makedirs(file_directory, exist_ok=True)

    file_location = f"docs/{file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())

    file_hash = hashlib.sha256(open(file_location, "rb").read()).hexdigest()

    new_document = Documents(
        filename=file.filename,
        filehash=file_hash,
        content_type=file.content_type,
    )
    db.add(new_document)
    db.commit()

    return DocumentPydantic.model_validate(
        {"filename": file.filename, "content_type": file.content_type}
    )


def get_all_documents(db: Session) -> List[DocumentPydantic]:
    """Get all documents"""
    documents = db.query(Documents).all()
    return documents if documents else None


def document_list(current_user, db: Session) -> List[DocumentPydantic]:
    """Get all documents from db if there exists none,
    raise relevant exceptions"""

    if current_user.role < 5:
        raise NoValidPermissionsException()

    documents = get_all_documents(db)
    if not documents:
        raise NoDocumentsFoundException()

    return [
        DocumentPydantic(
            filename=doc.filename, content_type=str(doc.content_type)
        )
        for doc in documents
    ]
