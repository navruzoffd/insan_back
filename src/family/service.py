import datetime
from operator import and_
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from src.database.database import Family, User, fetch_all
from src.family.schemas import FamilyModel

async def get_family_leaderboard(session: AsyncSession) -> list[FamilyModel]:
    result = []
    query = select(Family).order_by(Family.balance.desc())
    familis: list[Family] = await fetch_all(session, query)

    for family in familis:
        result.append(
            FamilyModel(
                name=family.name,
                balance=family.balance,
                members_count=len(await get_users_by_family(session, family.id)),
            )
        )

    return result

async def create_family(session: AsyncSession, name: str) -> Family:
    family = Family(name=name)
    session.add(family)
    await session.commit()
    return family


async def get_users_by_family(session: AsyncSession, family_id: int) -> User:
    query = select(User).where(User.family_id == family_id)
    return await fetch_all(session, query)