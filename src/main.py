from fastapi import FastAPI
from middlewares.handle_error import HandleError
from middlewares.track_history import TrackHistory
from routers import admin, login, transaction, user

app = FastAPI()

app.add_middleware(HandleError)
app.add_middleware(TrackHistory)

app.include_router(login.router)
app.include_router(user.router)
app.include_router(transaction.router)
app.include_router(admin.router)