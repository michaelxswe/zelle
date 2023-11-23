from datetime import datetime, timedelta

from fastapi import Depends, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

from middlewares.handle_error import ApplicationException
from utils.settings import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY

http_bearer = HTTPBearer()


def create_token(user_id: int):
    expires = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    encode = {"user_id": user_id, "exp": expires}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    return token


def validate_token(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
):
    try:
        token = credentials.credentials
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = decoded_token.get("user_id")

        return user_id

    except JWTError:
        raise ApplicationException(
            status_code=status.HTTP_401_UNAUTHORIZED, error="Invalid token."
        )
