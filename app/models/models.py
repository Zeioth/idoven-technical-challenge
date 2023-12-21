# SQLAlchemy models for DB

import uuid
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.dialects.postgresql import JSONB

Base = declarative_base()


def generate_uuid():
    return str(uuid.uuid4())


class ECGDBModel(Base):
    """
    Defines how an ECG (electrocardiogram) is stored into the database.

    A ECG can have 0 → n leads.

    FK constraints: Deleting a ecg deletes all its asociated leads.
    """
    __tablename__ = "ecgs"
    id = Column(String, primary_key=True, index=True, default=generate_uuid)
    user_id = Column(String, ForeignKey('users.username', ondelete='CASCADE'))
    date = Column(String)

    leads = relationship("LeadDBModel", back_populates="ecg",
                         cascade="all, delete-orphan", passive_deletes=True)
    user = relationship("UserDBModel", back_populates="ecgs")


class LeadDBModel(Base):
    """
    A lead that belongs to a ECG.

    This is a weak entity.
    """
    __tablename__ = "leads"
    id = Column(String, primary_key=True, index=True, default=generate_uuid)
    ecg_id = Column(String, ForeignKey('ecgs.id', ondelete='CASCADE'))
    name = Column(String)
    samples = Column(Integer, nullable=True)
    signal = Column(JSONB)

    ecg = relationship("ECGDBModel", back_populates="leads")


class UserDBModel(Base):
    """
    Defines how a UserModel is stored into the database.

    A user can have 0 → n ecgs.
    """
    __tablename__ = "users"
    username = Column(String, primary_key=True, index=True)
    password = Column(String)
    role = Column(String)

    ecgs = relationship("ECGDBModel", back_populates="user",
                        cascade="all, delete-orphan")
