from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.schema import RegisterSchema
from src.database.database import User, fetch_one
from src.utils import hash_password

async def create_user(session: AsyncSession, user: RegisterSchema) -> User:
    new_user = User(
            name=user.name,
            lastname=user.lastname,
            surname=user.surname,
            email=user.email,
            hashed_password=hash_password(user.password),
            role=user.role.value,
        )

    session.add(new_user)
    await session.commit()
    return new_user 


async def get_user_by_email(session: AsyncSession, email: str) -> User | None:
    query = select(User).where(User.email == email)
    result = await fetch_one(session, query)
    return result