from passlib.context import CryptContext
from datetime import timedelta, datetime
import jwt

# import os
from src.config import Config
import uuid
import logging

# jwt_secret_key = os.getenv("JWT_SECRET_KEY")

password_context = CryptContext(schemes=["bcrypt"])

ACCESS_TOKEN_EXPIRY = 3600


def generate_hash_password(password: str) -> str:
    hash_password = password_context.hash(password)

    return hash_password


def verify_password(password: str, hashed_password: str) -> bool:
    return password_context.verify(password, hashed_password)


def generate_token(
    user_data: dict, expiry_date: timedelta = None, refresh: bool = False
):
    payload = {}

    payload["user"] = user_data
    payload["exp"] = (
        datetime.now() + expiry_date
        if expiry_date is not None
        else timedelta(seconds=ACCESS_TOKEN_EXPIRY)
    )
    payload["jti"] = str(uuid.uuid4())
    payload["refresh"] = refresh

    token = jwt.encode(
        payload=user_data,
        key=Config.JWT_SECRET_KEY,
        algorithm=Config.JWT_ALGORITHM,
    )

    return token


def decode_token(token: str) -> dict:
    try:
        token_data = jwt.decode(
        jwt=token, key=Config.JWT_SECRET_KEY, algorithms=Config.JWT_ALGORITHM
        )
        return token_data

    except jwt.PyJWTError as e:
        logging.exception(e) 
        return None