from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from schemas import Status
from src.database.database import get_db
from src.auth.jwt import parse_jwt_user_data
from src.user.service import get_user_by_id

from src.family.schemas import AddMemberModel, FamilyModel, MakeFamilyModel
from src.family.service import create_family, get_family_leaderboard

router = APIRouter()


@router.get(
    "/leaderboard",
    response_model=list[FamilyModel],
)
async def get_posts(
    session: AsyncSession = Depends(get_db),
    _=Depends(parse_jwt_user_data),
):
    return await get_family_leaderboard(session)


@router.post("/make", response_model=Status)
async def make(
    data: MakeFamilyModel,
    session: AsyncSession = Depends(get_db),
    auth=Depends(parse_jwt_user_data),
):
    user = await get_user_by_id(session, auth.id)

    if user.family_id:
        raise HTTPException(status_code=400, detail="User already in family")

    family = await create_family(session, data.name)
    user.family_id = family.id
    await session.commit()
    return Status()


@router.post(
    "/add/member",
    response_model=Status,
)
async def add_member(
    data: AddMemberModel,
    session: AsyncSession = Depends(get_db),
    auth=Depends(parse_jwt_user_data),
):
    if data.id == auth.id:
        raise HTTPException(status_code=400, detail="You can't add yourself")
    
    user = await get_user_by_id(session, auth.id)
    member = await get_user_by_id(session, data.id)

    if not user.family_id:
        raise HTTPException(status_code=400, detail="On user not have family")

    if member.family_id:
        raise HTTPException(status_code=400, detail="Member already in family")

    member.family_id = user.family_id
    await session.commit()

    return Status()
