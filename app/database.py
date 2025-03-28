from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from config import DATABASE_URL


# создание асинхронного подключения к БД
engine = create_async_engine(
    url=DATABASE_URL,
    echo=True,
    pool_size=10,
    max_overflow=20,
)

# сессия для работы с БД
session_factory = async_sessionmaker(engine)

class Base(DeclarativeBase):
    pass



