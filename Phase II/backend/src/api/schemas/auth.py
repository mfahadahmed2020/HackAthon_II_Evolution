"""
Authentication API schemas
Pydantic models for request/response validation
"""

from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
from uuid import UUID
from typing import Optional


class UserRegister(BaseModel):
    """
    Request schema for user registration
    """
    email: EmailStr = Field(
        ...,
        max_length=255,
        example="user@example.com",
        description="User's email address (must be unique)"
    )
    password: str = Field(
        ...,
        min_length=8,
        max_length=100,
        example="SecureP@ss123",
        description="Password (min 8 chars, 1 uppercase, 1 lowercase, 1 digit, 1 special char)"
    )
    
    @validator('password')
    def validate_password_strength(cls, v):
        """Validate password meets strength requirements"""
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.islower() for c in v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        if not any(c in "!@#$%^&*(),.?\":{}|<>" for c in v):
            raise ValueError("Password must contain at least one special character")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "SecureP@ss123"
            }
        }


class UserLogin(BaseModel):
    """
    Request schema for user login
    """
    email: EmailStr = Field(
        ...,
        max_length=255,
        example="user@example.com",
        description="User's email address"
    )
    password: str = Field(
        ...,
        max_length=100,
        example="SecureP@ss123",
        description="User's password"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "SecureP@ss123"
            }
        }


class UserResponse(BaseModel):
    """
    Response schema for user information
    Excludes sensitive data (password, etc.)
    """
    id: UUID
    email: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "email": "user@example.com",
                "is_active": True,
                "created_at": "2026-03-14T10:30:00Z"
            }
        }


class TokenResponse(BaseModel):
    """
    Response schema for authentication token
    """
    access_token: str = Field(
        ...,
        description="JWT access token"
    )
    token_type: str = Field(
        ...,
        enum=["bearer"],
        description="Token type (always 'bearer')"
    )
    expires_in: int = Field(
        ...,
        description="Token expiration time in seconds"
    )
    user: UserResponse = Field(
        ...,
        description="Authenticated user information"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "expires_in": 86400,
                "user": {
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "email": "user@example.com",
                    "is_active": True,
                    "created_at": "2026-03-14T10:30:00Z"
                }
            }
        }


class MessageResponse(BaseModel):
    """
    Generic message response
    """
    detail: str = Field(
        ...,
        description="Response message"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "detail": "Operation successful"
            }
        }
