import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/postgres"
    DIRECT_URL: str = ""
    REDIS_URL: str = "redis://localhost:6379/0"
    OPENAI_API_KEY: str = ""

    class Config:
        env_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../.env")
        env_file_encoding = "utf-8"
        extra = "allow"

settings = Settings()
