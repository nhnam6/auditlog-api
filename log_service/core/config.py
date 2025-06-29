"""Configuration"""

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Settings"""

    app_name: str = "AuditLog API"
    DEBUG: bool = Field(False, env="DEBUG")
    LOG_LEVEL: str = "INFO"

    TENANT_ID: str = Field("1", env="TENANT_ID")

    DATABASE_URL: str = Field(..., env="DATABASE_URL")

    JWT_SECRET: str = Field(..., env="JWT_SECRET")
    JWT_ALGORITHM: str = Field("HS256", env="JWT_ALGORITHM")

    AWS_ENDPOINT_URL: str = Field(
        "http://localhost:4566",
        env="AWS_ENDPOINT_URL",
    )
    AWS_ACCESS_KEY_ID: str = Field("fake", env="AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY: str = Field("fake", env="AWS_SECRET_ACCESS_KEY")
    AWS_REGION: str = Field("ap-southeast-1", env="AWS_REGION")

    SQS_ENDPOINT: str = Field("http://localhost:4566", env="SQS_ENDPOINT")
    SQS_LOG_QUEUE_URL: str = Field(..., env="SQS_LOG_QUEUE_URL")
    SQS_EXPORT_QUEUE_URL: str = Field(..., env="SQS_EXPORT_QUEUE_URL")
    LOG_QUEUE_NAME: str = Field("log-queue", env="LOG_QUEUE_NAME")
    EXPORT_QUEUE_NAME: str = Field("export-queue", env="EXPORT_QUEUE_NAME")
    EXPORT_S3_BUCKET: str = Field("logs-export", env="EXPORT_S3_BUCKET")

    OPENSEARCH_HOST: str = Field(
        "http://localhost:9200",
        env="OPENSEARCH_HOST",
    )
    OPENSEARCH_PORT: int = Field(9200, env="OPENSEARCH_PORT")
    OPENSEARCH_USER: str = Field("admin", env="OPENSEARCH_USER")
    OPENSEARCH_PASS: str = Field("admin", env="OPENSEARCH_PASS")

    class Config:
        """Config"""

        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
