from fastapi import APIRouter, Depends, HTTPException, Response
from src.auth.schema import LoginSchema, RegisterSchema
from src.database.database import User
from src.utils import create_access_token, hash_password
from src.database.database import get_db
from src.database.logic import find_user_by_email
from src.utils import verify_password
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/auth",
                   tags=["Authentication"])

@router.post("")
async def registration_user(user_data: RegisterSchema, session: AsyncSession = Depends(get_db)):

    user = await find_user_by_email(session, user_data.email)

    if user:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = hash_password(user_data.password)

    new_user = User(
        name=user_data.name,
        lastname=user_data.lastname,
        surname=user_data.surname,
        email=user_data.email,
        hashed_password=hashed_password,
        role=user_data.role.value
    )

    session.add(new_user)
    await session.commit()
    return {"status": 200}


@router.post("/login")
async def login_user(log_user: LoginSchema, response: Response, session=Depends(get_db)):
    user = await find_user_by_email(session, log_user.email)

    if not user:
        raise HTTPException(status_code=404, detail="User does not exist")

    if not verify_password(log_user.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect password")

    token = create_access_token({"sub": str(user.id)})

    response.set_cookie("access_token", token)

    return {"status": 200}

@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("access_token")
    return  {"status": 200}