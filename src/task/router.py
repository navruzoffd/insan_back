from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.database import get_db
from src.auth.jwt import parse_jwt_user_data
from src.user.service import get_user_by_id

from src.task.schemas import TaskModel
from src.task.service import get_tasks, complete_task

router = APIRouter()


@router.get(
    "",
    response_model=list[TaskModel],
)
async def get_posts(
    session: AsyncSession = Depends(get_db),
    auth=Depends(parse_jwt_user_data),
):
    user = await get_user_by_id(session, auth.id)
    return await get_tasks(session, user.id)


@router.post("/complete")
async def complete(
    task_id: int,
    session: AsyncSession = Depends(get_db),
    auth=Depends(parse_jwt_user_data),
):
    user = await get_user_by_id(session, auth.id)
    return await complete_task(session, task_id, user)


