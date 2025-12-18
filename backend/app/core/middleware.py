import logging
import time
from uuid import uuid4

from fastapi import Request

logger = logging.getLogger(__name__)

async def request_logging_middleware(request: Request, call_next):
    request_id = uuid4().hex
    request.state.request_id = request_id

    user_id = getattr(request.state, "user_id", None)

    start_time = time.monotonic()
    response = await call_next(request)
    duration_ms = (time.monotonic() - start_time) * 1000

    client_host = request.client.host if request.client else "unknown"
    client_port = request.client.port if request.client else "unknown"
    headers = dict(request.headers)
    query_params = dict(request.query_params)

    logger.info(
        f"{request.method} {request.url.path} {response.status_code} "
        f"duration={duration_ms:.2f}ms request_id={request_id} user_id={user_id} "
        f"client={client_host}:{client_port} "
        f"query={query_params} headers={headers}"
    )

    return response
