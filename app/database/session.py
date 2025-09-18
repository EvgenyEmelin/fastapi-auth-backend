from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from fastapi import Depends



DATABASE_URL = 'postgresql+asyncpg://postgres:3554@localhost:5432/db'

engine = create_async_engine(DATABASE_URL, echo=True)

async_session = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)

Base = declarative_base()

async def get_db()-> AsyncSession:
    async with async_session() as session:
        yield session
