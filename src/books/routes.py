from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from src.books.schemas import Book, BookResponse, BookUpdateModel, BookCreateModel
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from .service import BookService


book_router = APIRouter()
book_service = BookService()


@book_router.get("/", response_model=BookResponse)
async def get_all_books(session: AsyncSession = Depends(get_session)):
    books = await book_service.get_all_books(session)
    return {
        "message": "Books fetched successfully!!",
        "data": books
    }


@book_router.post("/", status_code=status.HTTP_201_CREATED, response_model=Book)
async def create_book(
    book_data: BookCreateModel, session: AsyncSession = Depends(get_session)
) -> dict:
    print(book_data)
    new_book = await book_service.create_book(book_data, session)
    return new_book


@book_router.get("/{book_id}", response_model=Book | None)
async def get_single_book(
    book_id: str, session: AsyncSession = Depends(get_session)
):
    book = await book_service.get_book(book_id, session)
    if book:
        return book
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )


@book_router.patch("/{book_id}", response_model=Book | None)
async def update_book(
    book_id: str,
    book_update_data: BookUpdateModel,
    session: AsyncSession = Depends(get_session),
):
    updated_book = await book_service.update_book(book_id, book_update_data, session)

    if updated_book:
        return updated_book
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )


@book_router.delete("/{book_id}", status_code=status.HTTP_200_OK, response_model=Book | None)
async def delete_book(
    book_id: str, session: AsyncSession = Depends(get_session)
):
    deleted_book = await book_service.delete_book(book_id, session)

    if deleted_book:
        return deleted_book
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found!"
        )
