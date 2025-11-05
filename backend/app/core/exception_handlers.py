from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.core.exceptions import AppException
from app.utils.logger import logger

def setup_exception_handlers(app: FastAPI):
    """Global exception handlers registration."""

    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        log_func = getattr(logger, exc.log_level, logger.error)
        log_func(f"[{exc.error_code.upper()}] {exc.message} ({request.url.path})")
        
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "code": exc.error_code,
                    "message": exc.message,
                    "path": str(request.url.path),
                }
            },
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        logger.exception(f"Unhandled exception: {exc}")
        return JSONResponse(
            status_code=500,
            content={
                "error": {
                    "code": "internal_error",
                    "message": "Internal server error",
                    "path": request.url.path,
                }
            },
        )
