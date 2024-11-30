from fastapi import APIRouter
from database.database import fetch_one
from sqlalchemy.ext.asyncio import AsyncSession

from database.logic import find_user_by_id

router = APIRouter(prefix="/user",
                   tags=["User"])


@router.get()
async def get_user(user_id: str):
    user = await find_user_by_id(id=user_id)