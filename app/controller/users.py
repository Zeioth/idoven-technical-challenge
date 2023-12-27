# Controller for the user model

from config import config as c
from jose import jwt, JWTError
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from controller.db import db_service
from model.models import UserDBModel

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


class UserService:
    def __init__(self, db_service):
        self.db_service = db_service

    def get_current_user(self, token: str = Depends(oauth2_scheme),
                         db: Session = Depends(db_service.get_db)):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(
                token, c.SECRET_KEY, algorithms=[c.HASH_ALGORITHM])
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


# Singleton instance
user_service = UserService(db_service)
