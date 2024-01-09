from contextlib import asynccontextmanager

from config import Settings
from database.postgres.client import DatabaseClient
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from jose import JWTError
import middleware
import exception
from router import account, database, transaction
from sqlalchemy.exc import SQLAlchemyError


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting application...")
    yield
    await app.state.database_client.shutdown_database()
    print("Closing application")


def create_app(settings: Settings = Settings()):  # type: ignore
    app = FastAPI(lifespan=lifespan)
    app.state.settings = settings
    app.state.database_client = DatabaseClient(app.state.settings.DATABASE_URL)

    app.exception_handler(exception.HttpException)(exception.handle_http_exception)
    app.exception_handler(RequestValidationError)(exception.handle_request_validation_exception)
    app.exception_handler(JWTError)(exception.handle_jwt_exception)
    app.exception_handler(SQLAlchemyError)(exception.handle_database_exception)
    app.exception_handler(Exception)(exception.handle_exception)

    app.middleware("http")(middleware.process_time)

    app.include_router(database.router)
    app.include_router(transaction.router)
    app.include_router(account.router)

    return app


app = create_app()
