import uuid
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

class CustomException(Exception):
    def __init__(self, status_code: int, error: str):
        self.status_code = status_code
        self.error = error

def log_exception(error: str):
    error_id = str(uuid.uuid4())
    print(f"{error_id}: {error}")
    headers = {'X-Error-ID': error_id}
    return headers

async def unhandled_exception(request: Request, exc: Exception):
    headers = log_exception(str(exc))

    return JSONResponse(
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
        content = {"error": "Internal Server Error."},
        headers = headers
    )

async def validation_exception(request: Request, exc: RequestValidationError):
    headers = log_exception(str(exc))

    return JSONResponse(
        status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
        content = {"errors": exc.errors()},
        headers = headers
    )

async def custom_exception(request: Request, exc: CustomException):
    headers = log_exception(exc.error)
    
    return JSONResponse(
        status_code = exc.status_code,
        content = {'error': exc.error},
        headers = headers
    )