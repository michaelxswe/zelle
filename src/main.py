import uvicorn
from fastapi import FastAPI, HTTPException

from exceptions.general_exception import general_exception_handler
from exceptions.http_exception import http_exception_handler
from middlewares.logging_middleware import LoggingMiddleware
from routers.user_router import user_router
from routers.database_router import database_router
from routers.transaction_router import transaction_router


app = FastAPI()

app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)
app.add_middleware(LoggingMiddleware)
app.include_router(user_router)
app.include_router(database_router)
app.include_router(transaction_router)


def start():
    uvicorn.run(app="main:app", reload=True)


if __name__ == "__main__":
    start()
