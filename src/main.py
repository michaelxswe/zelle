from fastapi import FastAPI

from middlewares.handle_error import HandleError
from middlewares.track_history import TrackHistory
from routers.database_router import database_router
from routers.transaction_router import transaction_router
from routers.user_router import user_router

app = FastAPI()


app.add_middleware(HandleError)
app.add_middleware(TrackHistory)
app.include_router(user_router)
app.include_router(database_router)
app.include_router(transaction_router)
