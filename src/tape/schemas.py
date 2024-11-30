from pydantic import BaseModel

class AddPost(BaseModel): 
    title: str
    description: str
    photo: str | None
    reactions: int

class PostModel(AddPost):
    id: int
   




