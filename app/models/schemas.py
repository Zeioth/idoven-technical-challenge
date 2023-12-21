# Pydantic schemas for FastAPI

from pydantic import BaseModel
from typing import List, Optional


class LeadModel(BaseModel):
    id: Optional[str] = None
    name: str
    samples: Optional[int]
    signal: List[int]


class ECGModel(BaseModel):
    id: Optional[str] = None
    date: str
    leads: List[LeadModel]

    class Config:
        from_attributes = True


class UserModel(BaseModel):
    username: str
    password: str
    role: str
