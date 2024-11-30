from sqlalchemy import select
from src.database.database import SessionLocal, fetch_one
from src.database.database import User
from sqlalchemy.ext.asyncio import AsyncSession

async def find_user_by_email(session: AsyncSession, email: str):
    query = select(User).where(User.email == email)
    result = await fetch_one(session, query)
    return result

async def find_user_by_id(session: AsyncSession, id: str):
    query = select(User).where(User.id == id)
    result = await fetch_one(session, query)
    return result