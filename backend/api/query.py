from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from backend.exceptions import NoValidPermissionsException
from backend.service.oauth import get_current_user
from backend.service.query_service import query_service

query_router = APIRouter(
    prefix="/query",
    tags=["Query"],
    responses={
        200: {"description": "Success"},
        404: {"description": "Resource Not Found"},
        500: {"description": "Internal Server Error"},
    },
)


@query_router.get("/", dependencies=[Depends(get_current_user)])
async def query(query: str):
    """
    Handle query requests from user and
    return appropriate response
    """
    try:
        response = await query_service(query=query)
        return response
    except NoValidPermissionsException as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
