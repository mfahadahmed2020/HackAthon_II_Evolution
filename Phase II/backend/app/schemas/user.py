"""
User schemas for request/response validation
Pydantic schemas with password validation
"""

from pydantic import BaseModel, EmailStr, field_validator
import re


class UserCreate(BaseModel):
    """
    Schema for user registration request
    Validates email format and password strength
    """
    email: EmailStr
    password: str
    
    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        """
        Validate password meets security requirements:
        - Minimum 8 characters
        - At least one uppercase letter
        - At least one lowercase letter
        - At least one number
        - At least one special character
        """
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain uppercase letter")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain lowercase letter")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain a number")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise ValueError("Password must contain special character")
        return v


class UserRead(BaseModel):
    """
    Schema for user response
    Excludes sensitive password field
    """
    id: str
    email: str
    created_at: str  # datetime as ISO string
    
    class Config:
        from_attributes = True
