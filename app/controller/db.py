# Controller for the DB

from config import config as c
from jose import jwt
from passlib.hash import bcrypt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from databases import Database, DatabaseURL
from model.models import Base, UserDBModel


class DBService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DBService, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        DATABASE_URL = DatabaseURL(
            "postgresql://apiuser:apipassword@localhost/idovendb")
        self.database = Database(DATABASE_URL)
        self.engine = create_engine(str(DATABASE_URL))
        self.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine)

    async def connect_db(self):
        await self.database.connect()

    async def disconnect_db(self):
        await self.database.disconnect()

    def get_db(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()

    async def create_tables(self):
        Base.metadata.create_all(bind=self.engine)

    async def create_user(self, username: str, password: str, role: str):
        db: Session = next(self.get_db())

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
            token = jwt.encode(token_data, c.SECRET_KEY,
                               algorithm=c.HASH_ALGORITHM)
            print(f"Token for 'user': {token}")


# Singleton instance
db_service = DBService()
