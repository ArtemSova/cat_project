import hashlib
from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database import Base


class Cats(Base):
    __tablename__ = "cats"
    cat_id = Column(Integer, primary_key=True, index=True)
    cat_name = Column(String, index=True)
    cat_color = Column(String)
    cat_age = Column(Integer)
    cat_rating = Column(Integer, default=3)

class Users(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    user_tg_id = Column(Integer, unique=True, nullable=False)
    user_name = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    phone_number = Column(String)
    reg_time = Column(DateTime, server_default=func.now())





