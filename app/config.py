from pydantic import BaseSettings, AnyUrl
from app.database import DATABASE_URL
class Settings(BaseSettings):
    PROJECT_NAME: str = "Order Management System API"
    DATABASE_URL: str = DATABASE_URL
    SECRET_KEY: str = "7c4f2bdf9e1f4c8caa3f9c0f90a1b23d7dc4e6d81f947aa21d4fa2a7c9be32ef"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60  
    BCRYPT_ROUNDS: int = 12

    class Config:
        env_file = ".env"

settings = Settings()
