from fastapi import APIRouter, Depends, HTTPException

from src.database.database import get_db
from src.auth.jwt import parse_jwt_user_data
from src.user.service import get_user_by_id, get_user_by_name, get_user_family
from src.user.schemas import User, UserModel

router = APIRouter()


@router.get("", response_model=User)
async def get_user(
    auth=Depends(parse_jwt_user_data),
    session=Depends(get_db),
):
    user = await get_user_by_id(session, auth.id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    family = await get_user_family(session, user)
    return User(
        user=UserModel(
            id=user.id,
            name=user.name,
            lastname=user.lastname,
            surname=user.surname,
            email=user.email,
            role=user.role,
        ),
        family=[
            UserModel(
                id=member.id,
                name=member.name,
                lastname=member.lastname,
                surname=member.surname,
                email=member.email,
                role=member.role,
            )
            for member in family
        ],
    )


@router.get("/members", response_model=list[UserModel])
async def get_members(
    name: str,
    auth=Depends(parse_jwt_user_data),
    session=Depends(get_db),
):
    members = await get_user_by_name(session, name, exclude=[auth.id])

    return [
        UserModel(
            id=member.id,
            name=member.name,
            lastname=member.lastname,
            surname=member.surname,
            email=member.email,
            role=member.role,
        )
        for member in members
    ]
