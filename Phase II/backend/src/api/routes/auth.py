"""
Authentication routes
Endpoints for user registration, login, and token management
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from datetime import timedelta
import logging

from backend.src.core.database import get_session
from backend.src.core.config import settings
from backend.src.api.schemas.auth import (
    UserRegister,
    UserLogin,
    UserResponse,
    TokenResponse,
    MessageResponse,
)
from backend.src.services.user_service import UserService
from backend.src.services.token_service import create_access_token
from backend.src.services.password_service import validate_password_strength
from backend.src.core.validators import validate_email
from backend.src.models.user import User
from backend.src.api.dependencies import get_current_user

# Setup logging
logger = logging.getLogger(__name__)

# Create router with /api prefix
router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Create a new user account with email and password",
)
async def register(
    user_data: UserRegister,
    session: Session = Depends(get_session),
) -> User:
    """
    Register a new user account
    
    **Requirements:**
    - Email must be valid format and unique (case-insensitive)
    - Password must meet strength requirements:
      - At least 8 characters
      - At least one uppercase letter
      - At least one lowercase letter
      - At least one digit
      - At least one special character
    
    **Returns:**
    - Created user information (id, email, is_active, created_at)
    
    **Errors:**
    - 400: Invalid email format or weak password
    - 409: Email already registered
    - 500: Database error
    """
    # Validate email format
    is_valid, normalized_email, email_error = validate_email(user_data.email)
    if not is_valid:
        logger.warning(f"Registration attempt with invalid email: {email_error}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid email format: {email_error}",
        )
    
    # Validate password strength
    is_valid, password_error = validate_password_strength(user_data.password)
    if not is_valid:
        logger.warning(f"Registration attempt with weak password: {password_error}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Weak password: {password_error}",
        )
    
    try:
        # Create user
        user = UserService.create_user(session, user_data)
        
        logger.info(f"User registered successfully: {user.email} (ID: {user.id})")
        
        return user
        
    except ValueError as e:
        # Handle duplicate email or other validation errors
        error_msg = str(e)
        if "already registered" in error_msg:
            logger.warning(f"Registration attempt with existing email: {user_data.email}")
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered",
            )
        else:
            logger.error(f"Registration error: {error_msg}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_msg,
            )
    
    except Exception as e:
        # Handle database errors
        logger.error(f"Database error during registration: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database connection failed",
        )


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Login user",
    description="Authenticate user and receive JWT access token",
)
async def login(
    credentials: UserLogin,
    session: Session = Depends(get_session),
) -> TokenResponse:
    """
    Login with email and password
    
    **Returns:**
    - JWT access token (valid for 24 hours)
    - Token type (bearer)
    - Expiration time in seconds
    - User information
    
    **Errors:**
    - 401: Invalid credentials
    - 403: Account deactivated
    - 500: Database error
    """
    try:
        # Authenticate user
        user = UserService.authenticate_user(
            session,
            credentials.email,
            credentials.password,
        )
        
        if not user:
            logger.warning(f"Login attempt with invalid credentials: {credentials.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Check if user is active
        if not user.is_active:
            logger.warning(f"Login attempt with inactive account: {user.email}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is deactivated",
            )
        
        # Create access token
        access_token = create_access_token(
            user_id=user.id,
            email=user.email,
            expires_delta=timedelta(minutes=settings.JWT_EXPIRATION_MINUTES),
        )
        
        logger.info(f"User logged in successfully: {user.email} (ID: {user.id})")
        
        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=settings.JWT_EXPIRATION_MINUTES * 60,  # Convert to seconds
            user=UserResponse(
                id=user.id,
                email=user.email,
                is_active=user.is_active,
                created_at=user.created_at,
            ),
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    
    except Exception as e:
        # Handle database errors
        logger.error(f"Database error during login: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database connection failed",
        )


@router.get(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Get current user",
    description="Get information about the currently authenticated user",
)
async def get_me(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Get current authenticated user information
    
    **Requires:**
    - Valid JWT token in Authorization header
    
    **Returns:**
    - Current user information (id, email, is_active, created_at)
    
    **Errors:**
    - 401: Not authenticated or token expired
    - 404: User not found
    - 403: Account deactivated
    """
    logger.info(f"Current user accessed: {current_user.email} (ID: {current_user.id})")
    return current_user


@router.post(
    "/logout",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    summary="Logout user",
    description="Invalidate current token (client-side token removal)",
)
async def logout(
    current_user: User = Depends(get_current_user),
) -> MessageResponse:
    """
    Logout current user
    
    Note: JWT tokens are stateless, so logout is handled client-side
    by removing the token from storage. This endpoint is provided
    for future session management enhancements.
    
    **Requires:**
    - Valid JWT token in Authorization header
    
    **Returns:**
    - Success message
    """
    logger.info(f"User logged out: {current_user.email} (ID: {current_user.id})")
    
    return MessageResponse(
        detail="Successfully logged out. Please remove the token from your client storage."
    )
