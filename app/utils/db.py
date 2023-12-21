# Database adapter

from config import SECRET_KEY, HASH_ALGORITHM
from jose import jwt
from passlib.hash import bcrypt

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from databases import Database, DatabaseURL
from models.models import Base, UserDBModel


# Setup database
# -----------------------------------------------------------------------------
DATABASE_URL = DatabaseURL(
    "postgresql://apiuser:apipassword@localhost/idovendb")
database = Database(DATABASE_URL)
engine = create_engine(str(DATABASE_URL))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Start/Stop database
# -----------------------------------------------------------------------------
async def connect_db():
    await database.connect()


async def disconnect_db():
    await database.disconnect()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def create_tables():
    """
    Use the alchemy models schemas defined in models.py to create DB tables.
    """
    Base.metadata.create_all(bind=engine)


async def create_user(username: str, password: str, role: str):
    """
    Create an example user with permissions to use the ecgs endpoints.
    Also, generate a token for the user.

    This function is meant for development only.
    It can be safely removed.
    """
    db: Session = next(get_db())

    # Check if the user exists
    user = db.query(UserDBModel).filter_by(username=username).first()

    if not user:
        # Hash the password using Passlib
        hashed_password = bcrypt.hash(password)

        # If not, create the user with the hashed password and role
        user = UserDBModel(
            username=username, password=hashed_password, role=role)
        db.add(user)

        db.commit()
        db.refresh(user)
        print("User 'user' with role {role} created successfully.")

        # Generate a token for the user
        token_data = {"sub": user.username, "scopes": []}
        token = jwt.encode(token_data, SECRET_KEY, algorithm=HASH_ALGORITHM)
        print(f"Token for 'user': {token}")

    db.close()
