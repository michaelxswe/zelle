from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from jose import JWTError
from sqlalchemy.exc import SQLAlchemyError


class HttpException(Exception):
    def __init__(self, status_code: int, content: dict[str, str] | None = None, headers: dict[str, str] | None = None):
        self.status_code = status_code
        self.content = content
        self.headers = headers


class ExceptionHandler:
    async def handle_http_exception(self, request: Request, exc: HttpException):
        return JSONResponse(status_code=exc.status_code, content=exc.content, headers=exc.headers)

    async def handle_request_validation_exception(self, request: Request, exc: RequestValidationError):
        return JSONResponse(status_code=400, content={"message": "request validation error"})

    async def handle_jwt_exception(self, request: Request, exc: JWTError):
        return JSONResponse(status_code=401, content={"message": "invalid token"})

    async def handle_database_exception(self, request: Request, exc: SQLAlchemyError):
        return JSONResponse(status_code=500, content={"message": "database error"})

    async def handle_exception(self, request: Request, exc: Exception):
        return JSONResponse(status_code=500, content={"message": "internal servor error"})
