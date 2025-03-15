from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import BookCreateModel, BookUpdateModel
from .models import Book
from sqlmodel import select, desc


class BookService:
    async def get_all_books(self, session: AsyncSession):
        statement = select(Book).order_by(desc(Book.created_at))

        result = await session.exec(statement)

        return result.all()

    async def get_book(self, book_uid: str, session: AsyncSession):
        statement = select(Book).where(Book.uid == book_uid)

        result = await session.exec(statement)

        book = result.first()

        return book if book is not None else None

    async def create_book(self, book_data: BookCreateModel, session: AsyncSession):
        book_data_dict = book_data.model_dump()

        new_book = Book(
            **book_data_dict
        )

        session.add(new_book)
        await session.commit()

        return new_book

    async def update_book(
        self, book_uid: str, update_data: BookUpdateModel, session: AsyncSession
    ):
        book_to_update = await self.get_book(book_uid, session)

        if book_to_update is not None:
            update_data_dict = update_data.model_dump(exclude_unset=True) # Only include set values

            for k, v in update_data_dict.items():
                if v is not None:  # Only update non-None values
                    setattr(book_to_update, k, v)
            
            await session.commit()

            return book_to_update
        else:
            return None

    async def delete_book(self,book_uid:str, session: AsyncSession):
        book_to_delete = await self.get_book(book_uid, session)

        if book_to_delete is not None:
            await session.delete(book_to_delete)

            await session.commit()

            return book_to_delete
        else:
            return None


# if need to do this in sqlalchemy then will use this
# from sqlalchemy.future import select
# from sqlalchemy import desc
# from sqlalchemy.ext.asyncio import AsyncSession

# class BookService:
#     async def get_all_books(self, session: AsyncSession):
#         statement = select(Book).order_by(desc(Book.created_at))
#         result = await session.execute(statement)
#         return result.scalars().all()  # `.scalars()` extracts actual model instances

#     async def get_book(self, book_uid: str, session: AsyncSession):
#         statement = select(Book).where(Book.uid == book_uid)
#         result = await session.execute(statement)
#         return result.scalars().first()  # `.first()` returns a single instance

#     async def create_book(self, book_data: BookCreateModel, session: AsyncSession):
#         book_data_dict = book_data.dict()  # Pydantic's `dict()` method
#         new_book = Book(**book_data_dict)
#         session.add(new_book)
#         await session.commit()
#         return new_book

#     async def update_book(self, book_uid: str, update_data: BookUpdateModel, session: AsyncSession):
#         book_to_update = await self.get_book(book_uid, session)
#         if book_to_update:
#             update_data_dict = update_data.dict(exclude_unset=True)
#             for key, value in update_data_dict.items():
#                 setattr(book_to_update, key, value)

#             await session.commit()
#             return book_to_update
#         return None

#     async def delete_book(self, book_uid: str, session: AsyncSession):
#         book_to_delete = await self.get_book(book_uid, session)
#         if book_to_delete:
#             await session.delete(book_to_delete)
#             await session.commit()
#             return True
#         return False
