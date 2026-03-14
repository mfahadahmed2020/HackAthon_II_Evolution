"""
Password hashing service
Uses bcrypt for secure password hashing and verification
"""

import bcrypt
from typing import Optional


# Cost factor for bcrypt (higher = more secure but slower)
# 12 is a good balance for most applications
BCRYPT_COST_FACTOR = 12


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt
    
    Args:
        password: Plain text password to hash
        
    Returns:
        Bcrypt-hashed password with salt
        
    Example:
        >>> hashed = hash_password("SecureP@ss123")
        >>> isinstance(hashed, str)
        True
    """
    # Convert password to bytes
    password_bytes = password.encode('utf-8')
    
    # Generate salt with configured cost factor
    salt = bcrypt.gensalt(rounds=BCRYPT_COST_FACTOR)
    
    # Hash the password
    hashed = bcrypt.hashpw(password_bytes, salt)
    
    # Return as string
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash
    
    Args:
        plain_password: Plain text password to verify
        hashed_password: Bcrypt-hashed password to check against
        
    Returns:
        True if password matches, False otherwise
        
    Example:
        >>> hashed = hash_password("SecureP@ss123")
        >>> verify_password("SecureP@ss123", hashed)
        True
        >>> verify_password("WrongPassword", hashed)
        False
    """
    try:
        # Convert inputs to bytes
        password_bytes = plain_password.encode('utf-8')
        hashed_bytes = hashed_password.encode('utf-8')
        
        # Verify the password
        return bcrypt.checkpw(password_bytes, hashed_bytes)
    except Exception:
        # If any error occurs (e.g., invalid hash format), return False
        return False


def validate_password_strength(password: str) -> tuple[bool, Optional[str]]:
    """
    Validate password meets strength requirements
    
    Requirements:
    - At least 8 characters
    - At least one uppercase letter (A-Z)
    - At least one lowercase letter (a-z)
    - At least one digit (0-9)
    - At least one special character (!@#$%^&*(),.?":{}|<>)
    
    Args:
        password: Password to validate
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if password meets all requirements
        - error_message: None if valid, error description if invalid
        
    Example:
        >>> is_valid, error = validate_password_strength("SecureP@ss123")
        >>> is_valid
        True
        >>> error
        None
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not any(c.isupper() for c in password):
        return False, "Password must contain at least one uppercase letter"
    
    if not any(c.islower() for c in password):
        return False, "Password must contain at least one lowercase letter"
    
    if not any(c.isdigit() for c in password):
        return False, "Password must contain at least one digit"
    
    if not any(c in "!@#$%^&*(),.?\":{}|<>" for c in password):
        return False, "Password must contain at least one special character"
    
    return True, None
