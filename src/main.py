from contextlib import asynccontextmanager
from exception import (
    HTTPException,
    http_exception_handler,
    validation_exception_handler,
    unhandled_exception_handler,
    jwt_exception_handler,
    sqlalchemy_exception_handler,
)
from config import Settings
from database.manager import DatabaseManager
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from jose import JWTError
from middleware import request_trace
from router import database, auth, account, transaction
from service.account import AccountService
from service.auth import AuthService
from service.transaction import TransactionService
from sqlalchemy.exc import SQLAlchemyError


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting application")
    app.state.settings = Settings()  # type: ignore
    app.state.database_manager = DatabaseManager(app.state.settings)
    app.state.account_service = AccountService()
    app.state.auth_service = AuthService()
    app.state.transaction_service = TransactionService()
    yield
    await app.state.database_manager.shutdown()
    print("Closing application")


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
