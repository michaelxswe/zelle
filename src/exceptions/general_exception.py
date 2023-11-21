from fastapi import Request
from fastapi.responses import JSONResponse


async def general_exception_handler(request: Request, exc: Exception):
    print(
        "--------------------------------------------------------------------------------"
    )
    print(exc)
    print(
        "--------------------------------------------------------------------------------"
    )
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"},
    )
