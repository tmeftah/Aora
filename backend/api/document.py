from fastapi import APIRouter
from fastapi import File, UploadFile
from fastapi.responses import JSONResponse
from typing import List

document_router = APIRouter(prefix="/documents",
                            tags=["Documents"],
                            responses={
                                200: {"description": "Success"},
                                404: {"description": "Resource Not Found"},
                                500: {"description": "Internal Server Error"},
                            },)


@document_router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    This endpoint allows you to upload a single file. It reads the file's content
    and returns the filename and content type as a JSON response.
    """
    contents = await file.read()
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
        contents = await file.read()  # Read the file contents
        file_details.append({
            "filename": file.filename,
            "content_type": file.content_type
        })
    return JSONResponse(content={"files": file_details})
