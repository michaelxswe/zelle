from pydantic_settings import BaseSettings, SettingsConfigDict
from fastapi import Request


class Settings(BaseSettings):
    model_config = SettingsConfigDict(frozen=True)
    ENV: str
    DATABASE_URL: str
    DATABASE_KEY: str
    SECRET_KEY: str
    ALGORITHM: str


def get_settings(request: Request) -> Settings:
    return request.app.state.settings
