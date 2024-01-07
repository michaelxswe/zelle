from contextlib import asynccontextmanager

from config import Settings
from database.postgres.client import DatabaseClient
from exception_handler import ExceptionHandler, HttpException
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from jose import JWTError
from middleware import Middleware
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
    exception_handler = ExceptionHandler()
    middleware = Middleware()

    app.exception_handler(HttpException)(exception_handler.handle_http_exception)
    app.exception_handler(RequestValidationError)(exception_handler.handle_request_validation_exception)
    app.exception_handler(JWTError)(exception_handler.handle_jwt_exception)
    app.exception_handler(SQLAlchemyError)(exception_handler.handle_database_exception)
    app.exception_handler(Exception)(exception_handler.handle_exception)

    app.middleware("http")(middleware.process_time)

    app.include_router(database.router)
    app.include_router(transaction.router)
    app.include_router(account.router)

    return app


app = create_app()
