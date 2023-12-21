# Helpers for user management

from config import SECRET_KEY, HASH_ALGORITHM
from jose import jwt, JWTError
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from utils.db import get_db
from models.models import UserDBModel

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(
        token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Given a OAuth2 token, returns the current user.

    Args:
        token (str): A valid non-expired token that identifies a user.
        db (Session): SQLAlchemy database session.

    Returns:
        UserDBModel: The SQLAlchemy model object of the specified user.
    """
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[HASH_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(UserDBModel).filter(
        UserDBModel.username == username).first()
    if user is None:
        raise credentials_exception

    return user
