from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class settings(BaseSettings):
    # Database settings
    DB_URL: str

    # JWT settings
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS settings
    CORS_ORIGINS: list[str] = ["*"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"