from pydantic import BaseModel


class FamilyModel(BaseModel):
    name: str
    balance: int
    members_count: int


class MakeFamilyModel(BaseModel):
    name: str

class AddMemberModel(BaseModel):
    id: int