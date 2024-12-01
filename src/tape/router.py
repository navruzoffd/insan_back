from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.database import get_db
from src.auth.jwt import parse_jwt_user_data

from src.tape.schemas import AddPost, PostModel
from src.tape.service import get_all_posts, make_reaction, add_post
from src.user.service import get_user_by_id

router = APIRouter()


@router.get(
    "",
    response_model=list[PostModel],
)
async def get_posts(
    session: AsyncSession = Depends(get_db),
    _ = Depends(parse_jwt_user_data)
):
    posts = await get_all_posts(session)
    return [
        PostModel(
            id=post.id,
            title=post.title,
            description=post.description,
            photo=post.photo,
            reactions=post.reactions,
        )
        for post in posts
    ]


@router.post(
    "/reaction",
    response_model=PostModel,
)
async def add_reaction(
    post: PostModel,
    session: AsyncSession = Depends(get_db),
    _ = Depends(parse_jwt_user_data)
):
    await make_reaction(session, post)
    


@router.post("/add")
async def create_post(
    post: AddPost,
    session: AsyncSession = Depends(get_db),
    auth = Depends(parse_jwt_user_data)
):
    user = await get_user_by_id(session, auth.id)
    if not user.family_id:
        raise HTTPException(status_code=400, detail="User not in family")
    await add_post(session, post, auth.id)