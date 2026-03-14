"""
User model for authentication
Represents a registered user account with unique email and hashed password
"""

from sqlmodel import Field, SQLModel, Index
from datetime import datetime
from uuid import UUID, uuid4
from pydantic import EmailStr, validator


class UserBase(SQLModel):
    """Base User model with shared fields"""
    email: str = Field(
        max_length=255,
        unique=True,
        index=True,
        nullable=False,
        description="User's email address (case-insensitive unique)"
    )
    is_active: bool = Field(
        default=True,
        nullable=False,
        description="Whether the user account is active"
    )


class User(UserBase, table=True):
    """
    User table - stores registered user accounts
    """
    __tablename__ = "users"
    
    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        nullable=False,
        sa_column_kwargs={"server_default": "gen_random_uuid()"},
        description="Unique identifier for the user"
    )
    hashed_password: str = Field(
        max_length=255,
        nullable=False,
        description="Bcrypt-hashed password with salt"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        sa_column_kwargs={"server_default": "NOW()"},
        description="When the user was created"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        sa_column_kwargs={
            "server_default": "NOW()",
            "onupdate": datetime.utcnow
        },
        description="When the user was last updated"
    )
    
    class Config:
        table = True
        schema = "public"


class UserCreate(SQLModel):
    """Schema for creating a new user"""
    email: EmailStr = Field(
        max_length=255,
        description="User's email address"
    )
    password: str = Field(
        min_length=8,
        description="Password (min 8 characters)"
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


class UserResponse(SQLModel):
    """Schema for user response (excludes sensitive data)"""
    id: UUID
    email: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# Index for case-insensitive email uniqueness
# Note: This is created via migration/DDL, not in SQLModel
# CREATE UNIQUE INDEX ix_users_email_lower ON users (LOWER(email));
