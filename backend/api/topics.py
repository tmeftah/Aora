from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from backend.db.sessions import get_db
from backend.service.oauth import get_current_user
from backend.service.topics_service import get_all_topics


topic_router = APIRouter(
    prefix="/topics",
    tags=["Topics"],
    responses={
        200: {"description": "Success"},
        404: {"description": "Resource Not Found"},
        500: {"description": "Internal Server Error"},
    },
)


@topic_router.get("/", dependencies=[Depends(get_current_user)])
async def get_topics(
    db: Session = Depends(get_db),
):
    """Get all valid users"""

    try:
        return get_all_topics(db=db)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
