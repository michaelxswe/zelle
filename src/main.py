from config import settings
from contextlib import asynccontextmanager
from database.postgresql.manager import engine
from exception import (
    HTTPException,
    http_exception_handler,
    validation_exception_handler,
    unhandled_exception_handler,
    jwt_exception_handler,
    sqlalchemy_exception_handler,
)
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from jose import JWTError
from middleware import request_trace
from router import database, auth, account, transaction
from sqlalchemy.exc import SQLAlchemyError


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("starting up...")
    yield
    await engine(settings=settings()).dispose()
    print("shutting down...")


app = FastAPI(lifespan=lifespan)

app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)
app.add_exception_handler(JWTError, jwt_exception_handler)
app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)

app.middleware("http")(request_trace)

app.include_router(database.router)
app.include_router(auth.router)
app.include_router(transaction.router)
app.include_router(account.router)
