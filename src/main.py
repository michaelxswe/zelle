from exceptions import unhandled_exception, validation_exception, custom_exception, RequestValidationError, CustomException
from fastapi import FastAPI
from middlewares import RequestTrace
from routers.admin import admin
from routers.login import login
from routers.transaction import transaction
from routers.user import user

app = FastAPI()

middlewares = [RequestTrace]
exceptions = [
    (Exception, unhandled_exception),
    (RequestValidationError, validation_exception),
    (CustomException, custom_exception)
]

routers = [admin, login, transaction, user]

for middleware in middlewares:
    app.add_middleware(middleware)

for exception_type, exception_handler in exceptions:
    app.add_exception_handler(exception_type, exception_handler)

for router in routers:
    app.include_router(router)