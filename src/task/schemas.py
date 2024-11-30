from pydantic import BaseModel

class TaskModel(BaseModel):
    id: int
    title: str
    description: str
    photo: str | None
    points: int
    status: str



