from pydantic import BaseModel, Field
from datetime import datetime
import uuid


class UserCreateModel(BaseModel):
    username: str = Field(max_length=12)
    email: str = Field(max_length=40)
    first_name: str
    last_name: str
    password: str = Field(min_length=6)


class UserModel(BaseModel):
    uid: uuid.UUID
    username: str
    email: str
    first_name: str
    last_name: str
    is_verified: bool
    created_at: datetime
    updated_at: datetime

class UserLoginModel(BaseModel):
    email: str
    password: str