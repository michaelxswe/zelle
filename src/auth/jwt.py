from config import get_settings, Settings
from datetime import datetime, timedelta
from exceptions.excs import AppException
from fastapi import Depends, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

http_bearer = HTTPBearer()


def create_token(user_id: int, settings: Settings):
    expires = datetime.utcnow() + timedelta(minutes=30)
    encode = {"user_id": user_id, "exp": expires}
    token = jwt.encode(encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return token


def validate_token(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    settings: Settings = Depends(get_settings),
):
    try:
        token = credentials.credentials
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = decoded_token.get("user_id")
        return user_id

    except JWTError:
        raise AppException(status_code=status.HTTP_401_UNAUTHORIZED, message="Invalid token.")
