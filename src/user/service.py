from fastapi import HTTPException
from sqlalchemy import select, and_
from src.database.database import fetch_all, fetch_one
from src.database.database import User
from sqlalchemy.ext.asyncio import AsyncSession


async def get_user_by_id(session: AsyncSession, id: str) -> User:
    query = select(User).where(User.id == id)
    result = await fetch_one(session, query)

    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return result

async def get_user_family(session: AsyncSession, user: User) -> list[User]:
    if not user.family_id:
        return []
    query = select(User).where(and_(User.family_id == user.family_id, User.id != user.id))
    return await fetch_all(session, query)

async def get_user_by_name(session: AsyncSession, name: str, exclude: list[int]) -> list[User]:
    query = select(User).where(and_(User.name.ilike(f"%{name}%"), User.id.not_in(exclude), User.family_id.is_(None)))
    return await fetch_all(session, query)