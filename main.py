from fastapi import FastAPI
from src.family.router import router as family_router
from src.auth.router import router as auth_router
from src.user.router import router as user_router
from src.tape.router import router as tape_roter

app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(user_router, prefix="/user", tags=["User"])
app.include_router(tape_roter, prefix="/tape", tags=["Tape"])
app.include_router(family_router, prefix="/family", tags=["Family"])
