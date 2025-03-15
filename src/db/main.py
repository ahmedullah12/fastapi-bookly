from sqlmodel import create_engine, SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker

from src.config import Config



# creating a engine to connecting with database
async_engine = AsyncEngine(
    create_engine(url=Config.DATABASE_URL, echo=True)
)

# connecting with database
async def init_db():
    async with async_engine.begin() as conn:
        # if the models isn't imported any where then need to import here, otherwise not
        from src.books.models import Book
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session() -> AsyncSession:
    Session = sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async with Session() as session:
        yield session



# to do this in sqlalchemy
# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
# from sqlalchemy.orm import sessionmaker, declarative_base
# from src.config import Config

# # Define the base class for models (instead of SQLModel)
# Base = declarative_base()

# # Create async engine
# async_engine = create_async_engine(Config.DATABASE_URL, echo=True)

# # Initialize the database and create tables
# async def init_db():
#     async with async_engine.begin() as conn:
#         from src.books.models import Book  # Ensure models are imported
#         await conn.run_sync(Base.metadata.create_all)  # Change from SQLModel.metadata.create_all

# # Create session factory
# SessionLocal = sessionmaker(
#     bind=async_engine,
#     class_=AsyncSession,
#     expire_on_commit=False
# )

# # Dependency function to get a database session
# async def get_session() -> AsyncSession:
#     async with SessionLocal() as session:
#         yield session



# Key Differences from SQLModel
# ✅ Base = declarative_base() → Used instead of SQLModel.
# ✅ create_async_engine() → Used instead of create_engine().
# ✅ Base.metadata.create_all() → Used instead of SQLModel.metadata.create_all().
# ✅ sessionmaker(bind=async_engine, class_=AsyncSession) → Works the same way.