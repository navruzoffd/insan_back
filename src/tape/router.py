from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.database import get_db
from src.auth.jwt import parse_jwt_user_data

from src.tape.schemas import AddPost, PostModel
from src.tape.service import get_all_posts, make_reaction, add_post

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
    post = await make_reaction(session, post)
    return post


@router.post("/add")
async def create_post(
    post: AddPost,
    session: AsyncSession = Depends(get_db),
    auth = Depends(parse_jwt_user_data)
):
    await add_post(session, post, auth.id)