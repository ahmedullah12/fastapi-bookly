from .models import User
from .schemas import UserCreateModel
from .utils import generate_hash_password, verify_password
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

class UserService:
    async def get_user_by_email(self, email: str, session: AsyncSession):
        statement = select(User).where(User.email == email)

        result = await session.exec(statement)

        user = result.first()

        return user 
    
    async def user_exists(self, email, session: AsyncSession):
        user = await self.get_user_by_email(email, session)

        # if user is None:
        #     return False
        # else:
        #     return True

        return True if user is not None else False 
    
    async def create_user(self, user_data: UserCreateModel, session: AsyncSession):
        user_data_dict = user_data.model_dump()

        new_user = User(
            **user_data_dict
        )

        new_user.password = generate_hash_password(user_data_dict["password"])

        session.add(new_user)

        await session.commit()

        return new_user
    

# in sqlalchemy only
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.future import select

# class UserService:
#     @staticmethod
#     async def get_user_by_email(email: str, session: AsyncSession):
#         statement = select(User).where(User.email == email)

#         result = await session.execute(statement)

#         user = result.scalars().first()  # Extracts the first user object
        
#         return user
