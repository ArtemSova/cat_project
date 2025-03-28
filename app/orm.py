import hashlib
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import engine, session_factory
from app.models import Base, Users, Cats



async def init_db():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.create_all)
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

# --------------------------------------Функции для FastAPI-----------------------------------------------
async def get_db():
    async with session_factory() as db:
        yield db

async def all_cats():
    async with session_factory() as session:
        query = select(Cats)
        result = await session.execute(query)
        cats = result.scalars().all()
        return cats

async def new_cat(cat_name, cat_color, cat_age):
    async with session_factory() as session:
        cat = Cats(cat_name=cat_name, cat_color=cat_color, cat_age=cat_age)
        session.add(cat)
        session.commit()

async def all_users():
    async with session_factory() as session:
        query = select(Users.user_name, Users.password)
        result = await session.execute(query)
        users = result.all()
        return users


# ------------------------------------------Функции для бота----------------------------------------------------
async def orm_add_user(session: AsyncSession, user_tg_id: int, user_name: str, password: str, phone_number):
    obj = Users(
        user_tg_id=user_tg_id,
        user_name=user_name,
        password=password,
        phone_number=phone_number,
    )
    session.add(obj)
    await session.commit()

async def orm_change_password(session: AsyncSession, user_tg_id: int, password: str):
    query = update(Users).where(Users.user_tg_id == user_tg_id).values(password=password)
    await session.execute(query)
    await session.commit()

async def orm_add_new_cat(session: AsyncSession, data: dict):
    obj = Cats(
        cat_name=data["cat_name"],
        cat_color=data["cat_color"],
        cat_age=data["cat_age"],
    )
    session.add(obj)
    await session.commit()

async def orm_show_all_cats(session: AsyncSession):
    query = select(Cats)
    result = await session.execute(query)
    return result.scalars().all()


