from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(frozen=True)
    ENV: str
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str


@lru_cache
def settings():
    return Settings()  # type: ignore
