from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from backend.db.sessions import get_db
from backend.exceptions import NoValidPermissionsException
from backend.models.sqlalchemy_models import User
from backend.service.oauth import encrypt_password
from backend.service.oauth import get_current_user
from backend.service.user_service import fetch_user
from backend.service.user_service import get_all_user


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
    if current_user.id != user_id and current_user.role < 5:
        raise HTTPException(
            status_code=403, detail="Only admin users can view other users"
        )
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"username": user.username, "role": user.role}


@user_router.post("/")
async def create_user(
    username: str,
    password: str,
    role: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if current_user.role < 5:
        raise HTTPException(
            status_code=403, detail="Only admin users can create new users"
        )
    user = User(
        username=username, password_hash=encrypt_password(password), role=role
    )
    db.add(user)
    db.commit()
    return {"username": user.username, "role": user.role}


@user_router.put("/{user_id}")
async def update_user(
    user_id: int,
    username: str,
    password: str,
    role: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if current_user.id != user_id and current_user.role < 5:
        raise HTTPException(
            status_code=403, detail="Only admin users can update other users"
        )
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.username = username
    user.password = password
    user.role = role
    db.commit()
    return {"username": user.username, "role": user.role}


@user_router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    if current_user.id != user_id and current_user.role < 5:
        raise HTTPException(
            status_code=403, detail="Only admin users can delete other users"
        )

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"message": "User deleted"}
