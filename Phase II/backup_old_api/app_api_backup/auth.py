"""
Authentication endpoints for user registration and login
"""

from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.database import get_session
from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
)
from app.config import settings
from app.schemas.user import UserCreate, UserRead
from app.schemas.token import Token
from app.models.user import User
from app.core.exceptions import ErrorCodes, create_http_exception


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/signup", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserCreate,
    session: Session = Depends(get_session)
) -> User:
    """
    Register a new user account
    Validates email format, password strength, and checks for duplicate emails
    """
    # Check if email already exists
    existing_user = session.exec(
        select(User).where(User.email == user_data.email)
    ).first()
    
    if existing_user:
        raise create_http_exception(
            detail="Email already registered",
            status_code=status.HTTP_409_CONFLICT,
            error_code=ErrorCodes.EMAIL_ALREADY_EXISTS
        )
    
    # Hash password
    password_hash = get_password_hash(user_data.password)
    
    # Create user
    user = User(
        email=user_data.email,
        password_hash=password_hash
    )
    
    session.add(user)
    session.commit()
    session.refresh(user)
    
    return user


@router.post("/login", response_model=Token)
async def login(
    credentials: UserCreate,
    session: Session = Depends(get_session)
) -> dict:
    """
    Login with email and password
    Returns JWT access token valid for 24 hours
    """
    # Find user by email
    user = session.exec(
        select(User).where(User.email == credentials.email)
    ).first()
    
    # Verify user exists and password matches
    if not user or not verify_password(credentials.password, user.password_hash):
        raise create_http_exception(
            detail="Invalid email or password",
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_code=ErrorCodes.AUTH_INVALID_CREDENTIALS
        )
    
    # Create access token (24 hours)
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
