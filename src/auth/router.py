from fastapi import APIRouter, Depends, HTTPException

from src.auth.jwt import create_access_token
from src.database.database import get_db
from src.auth.service import create_user, get_user_by_email
from src.auth.schema import LoginSchema, RegisterSchema
from src.utils import verify_password


router = APIRouter()

@router.post("")
async def registration_user(
    user_data: RegisterSchema,
    session=Depends(get_db),
):
    user = await get_user_by_email(session, user_data.email)

    if user:
        raise HTTPException(status_code=400, detail="User already exists")

    user = await create_user(session, user_data)
    return {"status": "success", "token": create_access_token(user=str(user.id))}


@router.post("/login")
async def login_user(
    log_user: LoginSchema,
    session=Depends(get_db),
):
    user = await get_user_by_email(session, log_user.email)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(log_user.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect password")

    return {"status": "success", "token": create_access_token(user=str(user.id))}
