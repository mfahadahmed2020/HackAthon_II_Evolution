"""
Token schemas for authentication responses
"""

from pydantic import BaseModel


class Token(BaseModel):
    """
    Schema for authentication token response
    """
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """
    Schema for decoded JWT token payload
    """
    sub: str  # User ID
    exp: int  # Expiration timestamp
    iat: int  # Issued at timestamp
