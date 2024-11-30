from pydantic import PostgresDsn
from pydantic_settings import BaseSettings
from dotenv import load_dotenv


load_dotenv()

class Settings(BaseSettings):

    DATABASE_URL: PostgresDsn
    SECRET_KEY: str
    ALGORITHM: str


settings = Settings()