"""
Email validation utility
Uses email-validator library for RFC-compliant email validation
"""

from email_validator import validate_email as validate_email_lib, EmailNotValidError
from typing import Optional


def validate_email(email: str) -> tuple[bool, Optional[str], Optional[str]]:
    """
    Validate an email address format
    
    Args:
        email: Email address to validate
        
    Returns:
        Tuple of (is_valid, normalized_email, error_message)
        - is_valid: True if email is valid
        - normalized_email: Normalized email address if valid, None otherwise
        - error_message: None if valid, error description if invalid
        
    Example:
        >>> is_valid, normalized, error = validate_email("user@example.com")
        >>> is_valid
        True
        >>> normalized
        'user@example.com'
    """
    try:
        # Validate and normalize the email
        valid = validate_email_lib(
            email,
            check_deliverability=False,  # Don't check DNS/MX records
            allow_smtputf8=True,  # Allow internationalized email
        )
        
        # Return normalized email (lowercase)
        return True, valid.email.lower(), None
        
    except EmailNotValidError as e:
        # Email is invalid
        return False, None, str(e)
    
    except Exception as e:
        # Unexpected error
        return False, None, f"Validation error: {str(e)}"


def is_email_valid(email: str) -> bool:
    """
    Simple boolean check if email is valid
    
    Args:
        email: Email address to check
        
    Returns:
        True if valid, False otherwise
        
    Example:
        >>> is_email_valid("user@example.com")
        True
        >>> is_email_valid("invalid-email")
        False
    """
    is_valid, _, _ = validate_email(email)
    return is_valid


def normalize_email(email: str) -> Optional[str]:
    """
    Normalize an email address (lowercase, trimmed)
    
    Args:
        email: Email address to normalize
        
    Returns:
        Normalized email if valid, None if invalid
        
    Example:
        >>> normalize_email("User@Example.COM")
        'user@example.com'
    """
    _, normalized, _ = validate_email(email)
    return normalized


def emails_are_equal(email1: str, email2: str) -> bool:
    """
    Check if two email addresses are equal (case-insensitive)
    
    Args:
        email1: First email address
        email2: Second email address
        
    Returns:
        True if emails are equivalent, False otherwise
        
    Example:
        >>> emails_are_equal("user@example.com", "User@EXAMPLE.COM")
        True
    """
    norm1 = normalize_email(email1)
    norm2 = normalize_email(email2)
    
    if norm1 is None or norm2 is None:
        return False
    
    return norm1 == norm2
