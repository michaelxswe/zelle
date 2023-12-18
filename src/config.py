from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    model_config = SettingsConfigDict(frozen=True)
    ENV: str
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str


@lru_cache
def get_settings():
    return Settings()
