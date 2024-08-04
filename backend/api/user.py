
from fastapi import APIRouter, Depends, HTTPException
from backend.sqlalchemy_models import User, session
from backend.oauth import encrypt_password, get_current_user


user_router = APIRouter()



@user_router.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return {"username": current_user.username, "role": current_user.role}


@user_router.get("/users/")
async def read_users(current_user: User = Depends(get_current_user)):
    if current_user.role < 5:
        raise HTTPException(
            status_code=403, detail="Only admin users can view all users")
    return [{"username": user.username, "role": user.role} for user in session.query(User).all()]


@user_router.get("/users/{user_id}")
async def read_user(user_id: int, current_user: User = Depends(get_current_user)):
    if current_user.id != user_id and current_user.role < 5:
        raise HTTPException(
            status_code=403, detail="Only admin users can view other users")
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"username": user.username, "role": user.role}


@user_router.post("/users/")
async def create_user(username: str, password: str, role: int, current_user: User = Depends(get_current_user)):
    if current_user.role < 5:
        raise HTTPException(
            status_code=403, detail="Only admin users can create new users")
    user = User(username=username,
                password_hash=encrypt_password(password), role=role)
    session.add(user)
    session.commit()
    return {"username": user.username, "role": user.role}


@user_router.put("/users/{user_id}")
async def update_user(user_id: int, username: str, password: str, role: int, current_user: User = Depends(get_current_user)):
    if current_user.id != user_id and current_user.role < 5:
        raise HTTPException(
            status_code=403, detail="Only admin users can update other users")
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.username = username
    user.password = password
    user.role = role
    session.commit()
    return {"username": user.username, "role": user.role}


@user_router.delete("/users/{user_id}")
async def delete_user(user_id: int, current_user: User = Depends(get_current_user)):
    if current_user.id != user_id and current_user.role < 5:
        raise HTTPException(
            status_code=403, detail="Only admin users can delete other users")
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return {"message": "User deleted"}