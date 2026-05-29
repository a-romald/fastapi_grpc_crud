from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

import settings


DATABASE_URL = f"mysql+aiomysql://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

async_engine = create_async_engine(DATABASE_URL, echo=True)

async_session_maker = sessionmaker(
    async_engine, class_ = AsyncSession, expire_on_commit=False
)

class Base(DeclarativeBase):
    pass


# Dependency
async def get_async_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session


async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
