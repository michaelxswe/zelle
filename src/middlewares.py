from starlette.middleware.base import BaseHTTPMiddleware
import uuid

class RequestTrace(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        correlation_id = str(uuid.uuid4())
        request.state.correlation_id = correlation_id
        response = await call_next(request)
        return response