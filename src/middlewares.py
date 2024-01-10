import time

from fastapi import Request


async def process_time(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    end = time.time()
    print(end - start)
    return response
