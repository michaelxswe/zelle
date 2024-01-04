import uuid

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from jose import JWTError
from sqlalchemy.exc import SQLAlchemyError


class HTTPException(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message


def handle_exception(error: str):
    error_id = str(uuid.uuid4())
    print(f"{error_id}: {error}")
    headers = {"error_id": error_id}
    return headers


async def http_exception_handler(request: Request, e: HTTPException):
    return JSONResponse(status_code=e.status_code, content={"message": e.message})


async def validation_exception_handler(request: Request, e: RequestValidationError):
    return JSONResponse(status_code=400, content={"message": "validation error"})


async def jwt_exception_handler(request: Request, e: JWTError):
    return JSONResponse(status_code=401, content={"message": "invalid token"})


async def sqlalchemy_exception_handler(request: Request, e: SQLAlchemyError):
    return JSONResponse(status_code=500, content={"message": "database error"})


async def unhandled_exception_handler(request: Request, e: Exception):
    return JSONResponse(status_code=500, content={"message": "internal servor error"})
