from fastapi import APIRouter
from fastapi import HTTPException
from backend.service.query_service import query_service

query_router = APIRouter()


@query_router.get("/query")
async def query(query: str):
    """
    Handle query requests from user and
    return appropriate response
    """
    try:
        response = await query_service(query)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
