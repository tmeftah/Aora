from fastapi import APIRouter
from fastapi import Depends
from fastapi import File
from fastapi import HTTPException
from fastapi import UploadFile
from sqlalchemy.orm import Session

from backend.db.sessions import get_db
from backend.exceptions import NoDocumentsFoundException
from backend.models.sqlalchemy_models import User
from backend.service.document_service import document_list
from backend.service.document_service import save_document
from backend.service.oauth import get_current_user

# from fastapi.responses import JSONResponse
# from typing import List


document_router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
    responses={
        200: {"description": "Success"},
        404: {"description": "Resource Not Found"},
        500: {"description": "Internal Server Error"},
    },
)


@document_router.post("/upload", dependencies=[Depends(get_current_user)])
async def upload_file(
    current_user: User = Depends(get_current_user),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """
    This endpoint allows you to upload a single file.
    It reads the file's content, returns the filename
    and content type as a JSON response.
    """
    try:
        return save_document(file=file, db=db)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )


@document_router.get("/", dependencies=[Depends(get_current_user)])
def list_documents(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List all the documents which exist in db"""
    try:
        return document_list(db)

    except NoDocumentsFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# @document_router.post("/upload-multiple/")
# async def upload_multiple_files(files: List[UploadFile] = File(...)):
#     """
#     Upload multiple files.

#     This endpoint allows you to upload multiple files.
#     It reads the contents of each file and returns a list of
#     dictionaries containing the filenames and content types.
#     """
#     file_details = []
#     for file in files:
#         contents = await file.read()
#         print(contents)
#         file_details.append(
#             {"filename": file.filename, "content_type": file.content_type}
#         )
#     return JSONResponse(content={"files": file_details})
