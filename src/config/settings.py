from pathlib import Path

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class MyBaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra='ignore'
    )


class RedisSettings(MyBaseSettings):
    HOST: str = Field(alias="REDIS_HOST", default="redis")
    PORT: int = Field(alias="REDIS_PORT", default=6379)
    # USER: str = Field(alias="REDIS_USER")
    PASS: SecretStr = Field(alias="REDIS_PASS", default=None)

    @property
    def sync_url(self) -> str:
        return f"redis://:{self.PASS.get_secret_value()}@{self.HOST}:{self.PORT}/0"


class CelerySettings(MyBaseSettings):
    BROKER_URL: str = Field(
        default_factory=lambda: RedisSettings().sync_url
    )
    RESULT_BACKEND: str = Field(
        default_factory=lambda: RedisSettings().sync_url
    )

    TASK_SERIALIZER: str = Field(default="json")
    ACCEPT_CONTENT: list[str] = Field(default=["json"])
    RESULT_SERIALIZER: str = Field(default="json")
    TIMEZONE: str = Field(default="UTC")
    ENABLE_UTC: bool = Field(default=True)
    TASK_TRACK_STARTED: bool = Field(default=True)
    TASK_TIME_LIMIT: int = Field(default=60)  # 1 minute
    TASK_SOFT_TIME_LIMIT: int = Field(default=30)


class Settings(MyBaseSettings):
    redis_config: RedisSettings = Field(default_factory=RedisSettings)
    celery_config: CelerySettings = Field(default_factory=CelerySettings)

    DEBUG: bool = Field(alias="DEBUG", default=False)
    ENVIRONMENT: str = Field(alias="ENVIRONMENT", default="development")


settings = Settings()
