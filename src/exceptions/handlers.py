from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from exceptions.excs import AppException
import uuid


def handle_exception(error: str):
    error_id = str(uuid.uuid4())
    print(f"{error_id}: {error}")
    headers = {"X-Error-ID": error_id}
    return headers


async def app_exception_handler(request: Request, e: AppException):
    headers = handle_exception(e.message)
    return JSONResponse(status_code=e.status_code, content={"message": e.message}, headers=headers)


async def validation_exception_handler(request: Request, e: RequestValidationError):
    headers = handle_exception(e.errors())
    return JSONResponse(status_code=422, content={"message": e.errors()}, headers=headers)


async def unhandled_exception_handler(request: Request, e: Exception):
    headers = handle_exception(str(e))
    return JSONResponse(status_code=500, content={"message": str(e)}, headers=headers)
