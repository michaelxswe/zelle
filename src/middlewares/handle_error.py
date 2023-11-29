import uuid

from fastapi import status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware


def handle_error(error: str):
    error_id = str(uuid.uuid4())
    print(f"{error_id}: {error}")
    headers = {"X-Error-ID": error_id}
    return headers


class ApplicationException(Exception):
    def __init__(self, status_code: int, error: str):
        self.status_code = status_code
        self.error = error


class HandleError(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        try:
            response = await call_next(request)
            return response

        except ApplicationException as exc:
            headers = handle_error(exc.error)

            return JSONResponse(
                status_code=exc.status_code,
                content={"error": exc.error},
                headers=headers,
            )

        except RequestValidationError as exc:
            headers = handle_error(str(exc))

            return JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content={"errors": exc.errors()},
                headers=headers,
            )
        # except Exception as exc:
        #     headers = handle_error(str(exc))

        #     return JSONResponse(
        #         status_code=500,
        #         content={"error": "Internal Server Error."},
        #         headers=headers,
        #     )
