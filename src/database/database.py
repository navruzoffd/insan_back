from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.engine import make_url

from sqlalchemy import (
    Column,
    Integer,
    CursorResult,
    String,
    ForeignKey,
    DateTime,
    Select,
    Insert,
    Update,
)
from datetime import datetime

from typing import AsyncGenerator

from config import settings

DATABASE_URL = str(settings.DATABASE_URL)
url = make_url(DATABASE_URL)

async_engine = create_async_engine(url)
Base_a = declarative_base()


class Base(Base_a):
    __abstract__ = True

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


metadata = Base.metadata


SessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def fetch_one(session: AsyncSession, select_query: Select | Insert | Update):
    cursor: CursorResult = await session.execute(select_query)  # type: ignore
    return cursor.scalars().first()


async def fetch_all(
    session: AsyncSession, select_query: Select | Insert | Update
) -> list:
    cursor: CursorResult = await session.execute(select_query)  # type: ignore
    return [r for r in cursor.scalars().all()]


async def execute(session: AsyncSession, select_query: Insert | Update) -> None:
    return await session.execute(select_query)  # type: ignore


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False)
    family_id = Column(ForeignKey("family.id"), nullable=True)


class Family(Base):
    __tablename__ = "family"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    balance = Column(Integer, default=0)


class Task(Base):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    photo = Column(String)
    points = Column(Integer, nullable=False)


class FamilyTask(Base):
    __tablename__ = "family_task"

    id = Column(Integer, primary_key=True, autoincrement=True)
    family_id = Column(ForeignKey("family.id"), nullable=False)
    task_id = Column(ForeignKey("task.id"), nullable=False)
    status = Column(String)
    completed_at = Column(DateTime, default=None)


class Post(Base):
    __tablename__ = "post"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    description = Column(String)
    photo = Column(String)
    reactions = Column(Integer)
    creator = Column(ForeignKey("user.id"))


async def get_db() -> AsyncGenerator[SessionLocal, None]:  # type: ignore
    async with SessionLocal() as session:  # type: ignore
        try:
            yield session
        finally:
            await session.close()
