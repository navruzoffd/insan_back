from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import HTTPException

from src.database.database import Post, fetch_one, fetch_all
from src.tape.schemas import AddPost

async def get_all_posts(session: AsyncSession) -> list[Post]:
    query = select(Post)
    return await fetch_all(session, query)


async def make_reaction(session: AsyncSession, id: int) -> bool:
    post = await get_post(session, id)
    if post: 
        post.reactions += 1
        await session.commit()
    
    raise HTTPException(status_code=404, detail="Post not found")

async def get_post(session: AsyncSession, id: int) -> Post:
    query = select(Post).where(Post.id == id)
    result = await fetch_one(session, query)
    return result

async def add_post(session: AsyncSession, post: AddPost, user_id: int):
    session.add(
        Post(
            title=post.title,
            description=post.description,
            photo=post.photo,
            reactions=post.reactions,
            creator=user_id
            )
    )
    await session.commit()
    