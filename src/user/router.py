from fastapi import APIRouter, Depends, HTTPException
from database.database import get_db
from src.user.service import get_user_by_id, get_user_family
from src.user.schemas import UserModel, User

router = APIRouter()


@router.get("", responce_model = User)
async def get_user(user_id: str, session=Depends(get_db)):
    user = await get_user_by_id(session, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    family = await get_user_family(session, user)
    return User(user=user, family=family)