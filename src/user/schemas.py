from pydantic import BaseModel, EmailStr

class Family(BaseModel):
    id: int
    balance: int
    completed_tasks: int

class UserModel(BaseModel):
    id: int
    name: str
    lastname: str
    surname: str
    email: EmailStr
    role: str

class User(BaseModel):
    user: UserModel
    family: list[UserModel]