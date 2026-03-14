"""
Custom exceptions and error handlers
"""

from typing import Optional
from fastapi import HTTPException, status


# Error codes for consistent error responses
class ErrorCodes:
    """Application-wide error codes"""
    
    # Authentication errors
    AUTH_INVALID_CREDENTIALS = "AUTH_INVALID_CREDENTIALS"
    AUTH_TOKEN_EXPIRED = "AUTH_TOKEN_EXPIRED"
    AUTH_TOKEN_INVALID = "AUTH_TOKEN_INVALID"
    
    # Validation errors
    VALIDATION_ERROR = "VALIDATION_ERROR"
    
    # Resource errors
    RESOURCE_NOT_FOUND = "RESOURCE_NOT_FOUND"
    
    # Conflict errors
    EMAIL_ALREADY_EXISTS = "EMAIL_ALREADY_EXISTS"


def create_http_exception(
    detail: str,
    status_code: int = status.HTTP_400_BAD_REQUEST,
    error_code: Optional[str] = None
) -> HTTPException:
    """
    Create an HTTPException with consistent error format
    """
    if error_code:
        detail = f"{error_code}: {detail}"
    
    return HTTPException(
        status_code=status_code,
        detail=detail,
        headers={"X-Error-Code": error_code} if error_code else None
    )
