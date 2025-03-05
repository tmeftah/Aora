from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException


from backend.exceptions import ModelsNotRetrievedException
from backend.exceptions import NoValidPermissionsException
from backend.service.oauth import get_current_user
from backend.service.query_service import model_list
from backend.service.query_service import query_service
from typing import List

from fastapi import Query

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
async def query(query: str = Query(..., description="User query"),
                model_name: str = Query(..., description="Model to use"),
                # topics: List[str] = Query([], description="List of topics")
                ):
    """
    Handle query requests from user and
    return appropriate response
    """
    try:
        # topics = topics[0].split(",") if len(
        #     topics) == 1 and "," in topics[0] else topics
        response = await query_service(query=query, model_name=model_name)

        return response
    except NoValidPermissionsException as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@query_router.get("/list_models", dependencies=[Depends(get_current_user)])
async def get_downloaded_models():
    """Get all downloaded ollama models"""
    try:
        return await model_list()

    except ModelsNotRetrievedException as e:
        raise HTTPException(
            status_code=404, detail=f"Failed to retrieve models {e}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}"
        )
