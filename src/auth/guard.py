from config import Settings, get_settings
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt

http_bearer = HTTPBearer()


def validate_jwt(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    settings: Settings = Depends(get_settings),
):
    token = credentials.credentials
    claims = jwt.decode(token=token, key=settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    return claims
