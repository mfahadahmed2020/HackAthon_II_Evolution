"""
Authentication dependencies
JWT token validation and current user retrieval
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session
from typing import Optional
from uuid import UUID

from backend.src.core.database import get_session
from backend.src.services.token_service import verify_token, TokenData
from backend.src.services.user_service import UserService
from backend.src.models.user import User


# HTTP Bearer token security scheme
security = HTTPBearer(
    description="JWT token obtained from /api/auth/login endpoint",
    auto_error=False,
)


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    session: Session = Depends(get_session),
) -> User:
    """
    Dependency to get the current authenticated user from JWT token
    
    Usage:
        @router.get("/protected")
        def protected_route(current_user: User = Depends(get_current_user)):
            return {"user_id": current_user.id}
    
    Raises:
        HTTPException: 401 if not authenticated or token invalid/expired
        HTTPException: 403 if user account is inactive
        HTTPException: 404 if user not found
    
    Returns:
        Current authenticated User object
    """
    # Check if credentials provided
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Extract token
    token = credentials.credentials
    
    # Verify token
    token_data = verify_token(token)
    if token_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Get user from database
    user = UserService.get_user_by_id(session, token_data.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is deactivated",
        )
    
    return user


async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    session: Session = Depends(get_session),
) -> Optional[User]:
    """
    Dependency to optionally get the current user (doesn't require authentication)
    
    Usage:
        @router.get("/mixed")
        def mixed_route(current_user: Optional[User] = Depends(get_current_user_optional)):
            if current_user:
                return {"message": f"Hello {current_user.email}"}
            else:
                return {"message": "Hello anonymous"}
    
    Returns:
        Current User object if authenticated, None otherwise
    """
    if not credentials:
        return None
    
    token = credentials.credentials
    token_data = verify_token(token)
    
    if not token_data:
        return None
    
    user = UserService.get_user_by_id(session, token_data.user_id)
    if not user or not user.is_active:
        return None
    
    return user


async def get_current_user_id(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
) -> UUID:
    """
    Dependency to get just the current user ID from JWT token
    
    Usage:
        @router.get("/user-id")
        def get_user_id(current_user_id: UUID = Depends(get_current_user_id)):
            return {"user_id": str(current_user_id)}
    
    Raises:
        HTTPException: 401 if not authenticated or token invalid/expired
    
    Returns:
        Current user's UUID
    """
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = credentials.credentials
    token_data = verify_token(token)
    
    if token_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return token_data.user_id
