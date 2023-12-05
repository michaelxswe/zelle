from datetime import datetime, timedelta
from exceptions import CustomException
from fastapi import Depends, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

http_bearer = HTTPBearer()

SECRET_KEY = '09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7'
ALGORITHM = 'HS256'

def create_token(user_id: int):
    expires = datetime.utcnow() + timedelta(minutes = 30)
    encode = {"user_id": user_id, "exp": expires}
    token = jwt.encode(encode, SECRET_KEY, algorithm = ALGORITHM)
    return token

def validate_token(credentials: HTTPAuthorizationCredentials = Depends(http_bearer)):
    try:
        token = credentials.credentials
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
        user_id = decoded_token.get("user_id")
        return user_id

    except JWTError:
        raise CustomException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            error = "Invalid token."
        )