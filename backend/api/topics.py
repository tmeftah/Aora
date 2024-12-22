from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from backend.db.sessions import get_db
from backend.service.oauth import get_current_user
from backend.service.topics_service import get_all_topics
from backend.service.topics_service import create_topic
from backend.exceptions import DuplicateUserException


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

@topic_router.post("/", dependencies=[Depends(get_current_user)])
async def create_topics(
    name: str,
    db: Session = Depends(get_db),
):
    """Create a new topic"""
    try:
        return create_topic(
            db=db,
            name=name,
        )

    except DuplicateUserException as e:
        raise HTTPException(status_code=403, detail=str(e))

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail="Internal Server error",
            headers={"WWW-Authenticate": "Bearer"},
        )