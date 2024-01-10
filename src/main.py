from contextlib import asynccontextmanager

import exception_handlers
import exceptions
import middlewares
from config import Settings
from databases.postgres.client import DatabaseClient
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from jose import JWTError
from routers import account, database, transaction
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

    app.exception_handler(exceptions.HttpException)(exception_handlers.http_exception_handler)
    app.exception_handler(RequestValidationError)(exception_handlers.request_validation_exception_handler)
    app.exception_handler(JWTError)(exception_handlers.jwt_exception_handler)
    app.exception_handler(SQLAlchemyError)(exception_handlers.database_exception_handler)
    app.exception_handler(Exception)(exception_handlers.exception_handler)

    app.middleware("http")(middlewares.process_time)

    app.include_router(database.router)
    app.include_router(transaction.router)
    app.include_router(account.router)

    return app


app = create_app()
