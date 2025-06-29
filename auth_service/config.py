"""Configuration"""

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Settings"""

    app_name: str = "Auth Service"
    DEBUG: bool = Field(False, env="DEBUG")
    LOG_LEVEL: str = "INFO"

    DATABASE_URL: str = Field(..., env="DATABASE_URL")

    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        60,
        env="ACCESS_TOKEN_EXPIRE_MINUTES",
    )
    JWT_SECRET: str = Field(..., env="JWT_SECRET")
    JWT_ALGORITHM: str = Field("HS256", env="JWT_ALGORITHM")

    class Config:
        """Config"""

        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
