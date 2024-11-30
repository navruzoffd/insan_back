from fastapi import APIRouter

from fastapi import APIRouter, Depends
from src.database.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession


from src.tape.schemas import Post
router = APIRouter()


@router.get(
    "",
    response_model=list[Post],
)
def get_posts(
    session: AsyncSession = Depends(get_db),
):
    pass