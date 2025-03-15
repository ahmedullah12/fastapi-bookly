from pydantic import BaseModel
from typing import List, Optional
import uuid
from datetime import date, datetime

# this model is for response object
class Book(BaseModel):
    uid: uuid.UUID
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str
    created_at: datetime
    updated_at: datetime

# this model is for create object
class BookCreateModel(BaseModel):
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str

class BookResponse(BaseModel):
    message: str
    data: List[Book]

class BookUpdateModel(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    publisher: Optional[str] = None
    page_count: Optional[int] = None
    language: Optional[str] = None