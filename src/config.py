from pydantic_settings import BaseSettings, SettingsConfigDict
from fastapi import Request

class Settings(BaseSettings):
    model_config = SettingsConfigDict(frozen=True)
    ENV: str
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str


def get_settings(request: Request):
    return request.app.state.settings
