from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from backend.db.sessions import get_db
from backend.exceptions import DuplicateUserException
from backend.exceptions import NoTopicFoundException
from backend.service.oauth import get_current_user
from backend.service.topics_service import created_topic
from backend.service.topics_service import delete_topic_details
from backend.service.topics_service import get_all_topics
from backend.service.topics_service import get_topic_by_name
from backend.service.topics_service import update_topic


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


@topic_router.get("/{topic_name}", dependencies=[Depends(get_current_user)])
async def get_topic_id(
    topic_name: str,
    db: Session = Depends(get_db),
):
    """Get all topics by name"""

    try:
        return get_topic_by_name(name=topic_name, db=db)
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
        return created_topic(
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


@topic_router.put("/", dependencies=[Depends(get_current_user)])
async def update_topics(
    old_name: str,
    name: str,
    db: Session = Depends(get_db),
):
    """Create a new topic"""
    try:
        return update_topic(
            db=db,
            old_name=old_name,
            name=name,
        )

    except NoTopicFoundException as e:
        raise HTTPException(status_code=403, detail=str(e))

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail="Internal Server error",
            headers={"WWW-Authenticate": "Bearer"},
        )


@topic_router.delete("/{topic_name}", dependencies=[Depends(get_current_user)])
async def delete_topic(
    topic_name: str,
    db: Session = Depends(get_db),
):
    """Delete a specific topic"""
    try:
        return delete_topic_details(topic_name=topic_name, db=db)

    except NoTopicFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

    except Exception as e:
        print(e)  # remove later
        raise HTTPException(
            status_code=500,
            detail="Internal Server error",
            headers={"WWW-Authenticate": "Bearer"},
        )
