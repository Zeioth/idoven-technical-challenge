# API ENDPOINTS - User management

from config import SECRET_KEY, HASH_ALGORITHM
from jose import jwt
from passlib.hash import bcrypt

from sqlalchemy.orm import Session
from models.schemas import UserModel
from models.models import UserDBModel

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from utils.users import get_current_user
from utils.db import get_db


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/login")
async def get_login_token(
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    Login the user and return an access token.
    """

    username = form_data.username
    password = form_data.password

    db: Session = next(get_db())
    user = db.query(UserDBModel).filter_by(username=username).first()
    db.close()

    if not user or not user.password or not bcrypt.verify(
            password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Return token
    token_data = {"sub": username, "scopes": []}
    token = jwt.encode(token_data, SECRET_KEY, algorithm=HASH_ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}


@router.post("/create-user", tags=["users"])
async def create_user(
    user: UserModel,
    current_user: UserDBModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new user. Only users with the "admin" role can create new users.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")

    # Check if the user already exists
    existing_user = db.query(UserDBModel).filter(
        UserDBModel.username == user.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

    # Create a new user
    hashed_password = bcrypt.hash(user.password)
    db_user = UserDBModel(
        username=user.username, password=hashed_password, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {
        "message": "User created successfully",
        "username": db_user.username,
        "role": db_user.role
    }


@router.post("/delete-user/{username}", tags=["users"])
async def delete_user(
    username: str,
    current_user: UserDBModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a user. Only users with the "admin" role can delete users.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")

    # Check if the user exists
    user_to_delete = db.query(UserDBModel).filter(
        UserDBModel.username == username).first()

    if not user_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Delete the user
    db.delete(user_to_delete)
    db.commit()

    return {
        "message": "User deleted successfully",
        "username": username
    }
