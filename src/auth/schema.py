from pydantic import BaseModel, Field, EmailStr
from enum import Enum

class UserRole(Enum):
    father = "father"
    mother = "mother"

class RegisterSchema(BaseModel):
    name: str = Field(min_length=3, max_length=50)
    lastname: str = Field(min_length=3, max_length=50)
    surname: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=4, max_length=50)
    role: UserRole

class LoginSchema(BaseModel):
    email: EmailStr
    password: str = Field(min_length=4, max_length=50)

class JWTData(BaseModel):
    user: str
