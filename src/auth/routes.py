from fastapi import APIRouter, Depends, status
from .schemas import UserCreateModel, UserLoginModel
from .models import User
from .service import UserService
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.exceptions import HTTPException
from .utils import generate_token, decode_token, verify_password
from datetime import timedelta
from fastapi.responses import JSONResponse

auth_router = APIRouter()
user_service = UserService()


@auth_router.post("/signup", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreateModel, session: AsyncSession = Depends(get_session)
):
    email = user_data.email

    user_exists = await user_service.user_exists(email, session)

    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User already exists!!"
        )

    new_user = await user_service.create_user(user_data, session)

    return new_user


@auth_router.post("/login")
async def login(
    login_data: UserLoginModel, session: AsyncSession = Depends(get_session)
):
    email = login_data.email
    password = login_data.password

    user = await user_service.get_user_by_email(email, session)

    if user is not None:
        password_correct = verify_password(password, user.password)

        if password_correct:
            access_token = generate_token(
                user_data={"email": user.email, "user_uid": str(user.uid)},
            )

            refresh_token = generate_token(
                user_data={"email": user.email, "user_uid": str(user.uid)},
                refresh=True,
                expiry_date=timedelta(days=30),
            )

            return JSONResponse(
                content={
                    "message": "Logged in successfully!!",
                    "access_token": access_token,
                    "refresh_token": refresh_token
                }
            )
