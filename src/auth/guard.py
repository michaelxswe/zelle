from datetime import datetime, timedelta

from database.model import AccountModel
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt
from schema.token import AccessToken

http_bearer = HTTPBearer()


def get_access_token(credentials: HTTPAuthorizationCredentials = Depends(http_bearer)):
    access_token = credentials.credentials
    return access_token


def create_access_token(account: AccountModel, key: str, algorithm: str):
    exp = datetime.utcnow() + timedelta(minutes=30)
    encode = {"account_id": account.id, "exp": exp}
    token = jwt.encode(claims=encode, key=key, algorithm=algorithm)
    return AccessToken(type="bearer", token=token)


def validate_access_token(token: str, key: str, algorithms: list[str]):
    claims = jwt.decode(token=token, key=key, algorithms=algorithms)
    return claims
