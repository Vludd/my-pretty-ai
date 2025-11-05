from fastapi import status

class RepositoryError(Exception):
    """Error in working with the database or storage."""
    def __init__(self, message: str, original: Exception | None = None):
        self.original = original
        super().__init__(message)

class AppException(Exception):
    """Base class for all business exceptions."""
    status_code: int = status.HTTP_400_BAD_REQUEST
    error_code: str = "app_error"
    message: str = "An unexpected error occurred"
    log_level: str = "error"  # 'debug', 'info', 'warning', 'error', 'critical'

    def __init__(self, message: str | None = None, error_code: str | None = None, log_level: str | None = None):
        if message:
            self.message = message
        if error_code:
            self.error_code = error_code
        if log_level:
            self.log_level = log_level
        super().__init__(self.message)


class NotFoundException(AppException):
    status_code = status.HTTP_404_NOT_FOUND
    error_code = "not_found"
    message = "Resource not found"


class UnauthorizedException(AppException):
    status_code = status.HTTP_401_UNAUTHORIZED
    error_code = "unauthorized"
    message = "Authentication required"


class ForbiddenException(AppException):
    status_code = status.HTTP_403_FORBIDDEN
    error_code = "forbidden"
    message = "Access denied"


class ValidationException(AppException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    error_code = "validation_error"
    message = "Validation failed"


class InternalServerException(AppException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    error_code = "internal_server_error"
    message = "Internal Server Error"
