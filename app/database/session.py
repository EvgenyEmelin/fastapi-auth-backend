from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import event
from app.database.base import Base
from app.core.config import settings

DATABASE_URL = settings.database_url

engine = create_async_engine(
    settings.database_url,
    echo=True,
    pool_size=10,
    max_overflow=20,
    pool_recycle=1800,
    pool_pre_ping=True
)

@event.listens_for(engine.sync_engine, "connect")
def do_connect(dbapi_connection, connection_record):
    # Дополнительная конфигурация соединения при необходимости
    pass

async_session = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

async def get_db():
    async with async_session() as session:
        yield session

async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session
