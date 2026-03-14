"""
JWT token service
Creates and verifies JWT access tokens using python-jose
"""

from datetime import datetime, timedelta
from typing import Optional, Any
from jose import JWTError, jwt
from uuid import UUID
from pydantic import BaseModel

from backend.src.core.config import settings


class TokenPayload(BaseModel):
    """JWT token payload structure"""
    sub: str  # User ID (subject)
    email: str
    type: str = "access"
    exp: datetime
    iat: datetime


class TokenData(BaseModel):
    """Parsed token data"""
    user_id: UUID
    email: str
    token_type: str
    expires_at: datetime
    issued_at: datetime


def create_access_token(
    user_id: UUID,
    email: str,
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create a JWT access token for a user
    
    Args:
        user_id: User's unique identifier
        email: User's email address (included in token for convenience)
        expires_delta: Optional custom expiration time (defaults to JWT_EXPIRATION_MINUTES)
        
    Returns:
        Encoded JWT token string
        
    Example:
        >>> from uuid import uuid4
        >>> token = create_access_token(uuid4(), "user@example.com")
        >>> isinstance(token, str)
        True
        >>> len(token) > 0
        True
    """
    # Set expiration time
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.JWT_EXPIRATION_MINUTES
        )
    
    # Create token payload
    payload = {
        "sub": str(user_id),  # Subject (user ID)
        "email": email,
        "type": "access",
        "exp": expire,
        "iat": datetime.utcnow(),
    }
    
    # Encode and return token
    token = jwt.encode(
        payload,
        settings.BETTER_AUTH_SECRET,
        algorithm=settings.JWT_ALGORITHM
    )
    
    return token


def verify_token(token: str) -> Optional[TokenData]:
    """
    Verify and decode a JWT token
    
    Args:
        token: JWT token string to verify
        
    Returns:
        TokenData if token is valid, None if invalid or expired
        
    Example:
        >>> token_data = verify_token("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")
        >>> if token_data:
        ...     print(f"User ID: {token_data.user_id}")
        ...     print(f"Email: {token_data.email}")
    """
    try:
        # Decode and verify the token
        payload = jwt.decode(
            token,
            settings.BETTER_AUTH_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )
        
        # Extract token data
        user_id = UUID(payload.get("sub"))
        email = payload.get("email")
        token_type = payload.get("type", "access")
        expires_at = datetime.fromtimestamp(payload.get("exp"))
        issued_at = datetime.fromtimestamp(payload.get("iat"))
        
        # Validate required fields
        if user_id is None or email is None:
            return None
        
        # Validate token type
        if token_type != "access":
            return None
        
        return TokenData(
            user_id=user_id,
            email=email,
            token_type=token_type,
            expires_at=expires_at,
            issued_at=issued_at,
        )
        
    except (JWTError, ValueError, KeyError):
        # Token is invalid or expired
        return None


def is_token_expired(token: str) -> bool:
    """
    Check if a token is expired without fully decoding it
    
    Args:
        token: JWT token string
        
    Returns:
        True if token is expired, False otherwise
        
    Note:
        Returns True for invalid tokens as well
    """
    token_data = verify_token(token)
    if token_data is None:
        return True
    
    return token_data.expires_at < datetime.utcnow()


def get_token_expiration(token: str) -> Optional[datetime]:
    """
    Get the expiration time of a token
    
    Args:
        token: JWT token string
        
    Returns:
        Expiration datetime if valid, None if invalid
    """
    token_data = verify_token(token)
    if token_data is None:
        return None
    
    return token_data.expires_at
