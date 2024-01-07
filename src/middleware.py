import time
from fastapi import Request


class Middleware:
    async def process_time(self, request: Request, call_next):
        start = time.time()
        response = await call_next(request)
        end = time.time()
        print(end - start)
        return response