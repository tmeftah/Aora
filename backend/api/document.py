import hashlib
import os
from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import File
from fastapi import UploadFile
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from backend.db.sessions import get_db
from backend.models.sqlalchemy_models import Documents

document_router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
    responses={
        200: {"description": "Success"},
        404: {"description": "Resource Not Found"},
        500: {"description": "Internal Server Error"},
    },
)


@document_router.post("/upload")
async def upload_file(
    file: UploadFile = File(...), db: Session = Depends(get_db)
):
    """
    This endpoint allows you to upload a single file.
    It reads the file's content, returns the filename
    and content type as a JSON response.
    """
    file_directory = "docs"
    os.makedirs(file_directory, exist_ok=True)

    file_location = f"docs/{file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())

    file_hash = hashlib.sha256(open(file_location, "rb").read()).hexdigest()

    new_document = Documents(filename=file.filename, filehash=file_hash)
    db.add(new_document)
    db.commit()
    return {"filename": file.filename, "content_type": file.content_type}


@document_router.post("/upload-multiple/")
async def upload_multiple_files(files: List[UploadFile] = File(...)):
    """
    Upload multiple files.

    This endpoint allows you to upload multiple files.
    It reads the contents of each file and returns a list of
    dictionaries containing the filenames and content types.
    """
    file_details = []
    for file in files:
        contents = await file.read()
        print(contents)
        file_details.append(
            {"filename": file.filename, "content_type": file.content_type}
        )
    return JSONResponse(content={"files": file_details})
