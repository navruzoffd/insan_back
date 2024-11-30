from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.database import User, fetch_one
# from src.tape.schemas import 
from src.utils import hash_password