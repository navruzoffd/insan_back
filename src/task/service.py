import datetime
from operator import and_
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from src.database.database import Family, Post, Task, FamilyTask, User, fetch_one, fetch_all
from src.task.schemas import TaskModel


async def get_tasks(session: AsyncSession, family_id: int) -> list[TaskModel]:
    result = []
    family_tasks = await get_family_tasks(session, family_id)

    for family_task in family_tasks:
        task = await get_task(session, family_task.task_id)
        result.append(
            TaskModel(
                id=task.id,
                title=task.name,
                description=task.description,
                photo=task.photo,
                points=task.points,
                status=family_task.status,
            )
        )

    return family_tasks


async def complete_task(session: AsyncSession, task_id: int, user: User) -> bool:
    task = await get_task(session, task_id)
    family = await get_family(session, user.family_id)
    family_task = await get_family_task(session, user.family_id, task_id)

    if family_task.status != "completed":
        family_task.status = "completed"
        family.balance += task.points
        family_task.completed_at = datetime.datetime.now()
        return True
    return False

async def get_family_tasks(session: AsyncSession, family_id: int) -> list[FamilyTask]:
    query = select(FamilyTask).where(FamilyTask.family_id == family_id)
    return await fetch_all(session, query)

async def get_family_task(session: AsyncSession, family_id: int, task_id: int) -> FamilyTask:
    query = select(FamilyTask).where(and_(FamilyTask.family_id == family_id, FamilyTask.task_id == task_id))
    return await fetch_one(session, query)

async def get_family(session: AsyncSession, family_id: int) -> Family:
    query = select(Family).where(Family.id == family_id)
    return await fetch_one(session, query)

async def get_task(session: AsyncSession, id: int) -> Task:
    query = select(Task).where(Task.id == id)
    result = await fetch_one(session, query)
    return result
