from exceptions import HttpException
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from jose import JWTError
from sqlalchemy.exc import SQLAlchemyError


async def http_exception_handler(request: Request, exc: HttpException):
    return JSONResponse(status_code=exc.status_code, content=exc.content, headers=exc.headers)


async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=400, content={"message": "request validation error"})


async def jwt_exception_handler(request: Request, exc: JWTError):
    return JSONResponse(status_code=401, content={"message": "invalid token"})


async def database_exception_handler(request: Request, exc: SQLAlchemyError):
    return JSONResponse(status_code=500, content={"message": "database error"})


async def exception_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"message": "internal servor error"})
