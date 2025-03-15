from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
import uuid
from datetime import datetime


class User(SQLModel, table=True):
    __tablename__ = "users"
    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )
    username: str
    email: str
    first_name: str
    last_name: str
    is_verified: bool = Field(default=False)
    password: str = Field(exclude=True) # don't add that to response
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now, onupdate=datetime.now))

    def __repr__(self):
        return f"<User {self.username}>"
    

# in sqlalchemy only
# from sqlalchemy import Column, String, Boolean, TIMESTAMP, func
# from sqlalchemy.dialects.postgresql import UUID
# from sqlalchemy.orm import DeclarativeBase
# import uuid

# # Define a base class
# class Base(DeclarativeBase):
#     pass

# # Define the User model
# class User(Base):
#     __tablename__ = "users"

#     uid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
#     username = Column(String, unique=True, nullable=False, index=True)
#     email = Column(String, unique=True, nullable=False, index=True)
#     first_name = Column(String, nullable=False)
#     last_name = Column(String, nullable=False)
#     is_verified = Column(Boolean, default=False, nullable=False)
#     password = Column(String, nullable=False)  # Store hashed passwords
#     created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
#     updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

#     def __repr__(self):
#         return f"<User {self.username}>"
