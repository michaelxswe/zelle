from exceptions.excs import AppException
from exceptions.handlers import (
    app_exception_handler,
    validation_exception_handler,
    unhandled_exception_handler,
)
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from middlewares import trace
from routers import admin, login, user, transaction


async def lifespan(app: FastAPI):
    print("starting up...")
    yield
    print("shutting down...")


app = FastAPI(lifespan=lifespan)

app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)

app.add_middleware(trace.Trace)

app.include_router(admin.router)
app.include_router(login.router)
app.include_router(transaction.router)
app.include_router(user.router)
