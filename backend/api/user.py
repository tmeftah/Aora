from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from backend.db.sessions import get_db
from backend.exceptions import DuplicateUserException
from backend.exceptions import NoValidPermissionsException
from backend.exceptions import UserNotFoundException
from backend.models.sqlalchemy_models import User
from backend.service.oauth import get_current_user
from backend.service.user_service import created_user
from backend.service.user_service import delete_user_details
from backend.service.user_service import fetch_user
from backend.service.user_service import get_all_user
from backend.service.user_service import get_user_details
from backend.service.user_service import update_user_details


user_router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={
        200: {"description": "Success"},
        404: {"description": "Resource Not Found"},
        500: {"description": "Internal Server Error"},
    },
)


@user_router.get("/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    """Get current user"""
    return fetch_user(current_user)


@user_router.get("/")
async def get_users(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get all valid users"""

    try:
        return get_all_user(current_user, db)
    except NoValidPermissionsException as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )


@user_router.get("/{user_id}")
async def read_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:

        return get_user_details(current_user, db, user_id)

    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e)) from e

    except Exception as e:
        raise HTTPException(
            status_code=403,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        ) from e


@user_router.post("/")
async def create_user(
    username: str,
    password: str,
    role: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new user"""
    try:
        return created_user(current_user, db, username, password, role)

    except NoValidPermissionsException as e:
        raise HTTPException(status_code=403, detail=str(e))

    except DuplicateUserException as e:
        raise HTTPException(status_code=403, detail=str(e))

    except Exception as e:
        print(e)  # remove later
        raise HTTPException(
            status_code=500,
            detail="Internal Server error",
            headers={"WWW-Authenticate": "Bearer"},
        )


@user_router.put("/{user_id}")
async def update_user(
    user_id: int,
    username: str,
    password: str,
    role: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        return update_user_details(
            current_user=current_user,
            db=db,
            user_id=user_id,
            username=username,
            password=password,
            role=role,
        )

    except NoValidPermissionsException as e:
        raise HTTPException(status_code=403, detail=str(e))

    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

    except Exception as e:
        print(e)  # remove later
        raise HTTPException(
            status_code=500,
            detail="Internal Server error",
            headers={"WWW-Authenticate": "Bearer"},
        )


@user_router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete a specific user"""
    try:
        return delete_user_details(
            user_id=user_id, current_user=current_user, db=db
        )

    except NoValidPermissionsException as e:
        raise HTTPException(status_code=403, detail=str(e))

    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

    except Exception as e:
        print(e)  # remove later
        raise HTTPException(
            status_code=500,
            detail="Internal Server error",
            headers={"WWW-Authenticate": "Bearer"},
        )
