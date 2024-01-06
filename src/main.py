from contextlib import asynccontextmanager

from config import Settings
from database.client import DatabaseClient
from exception import (
    HttpException,
    http_exception_handler,
    jwt_exception_handler,
    sqlalchemy_exception_handler,
    unhandled_exception_handler,
    validation_exception_handler,
)
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from jose import JWTError
from middleware import request_trace
from router import account, database, transaction
from sqlalchemy.exc import SQLAlchemyError


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting application...")
    yield
    await app.state.database_client.shutdown_database()
    print("Closing application")


# factory set up to avoid mocking/patching during tests
def create_app(settings: Settings = Settings()):  # type: ignore
    app = FastAPI(lifespan=lifespan)
    app.state.settings = settings
    app.state.database_client = DatabaseClient(app.state.settings.DATABASE_URL)

    app.add_exception_handler(HttpException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)
    app.add_exception_handler(JWTError, jwt_exception_handler)
    app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)

    app.middleware("http")(request_trace)

    app.include_router(database.router)
    app.include_router(transaction.router)
    app.include_router(account.router)

    return app


app = create_app()
