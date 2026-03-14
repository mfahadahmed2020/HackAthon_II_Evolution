"""
User service
Handles user-related business logic: creation, authentication, lookup
"""

from sqlmodel import Session, select
from typing import Optional
from datetime import datetime
from uuid import UUID

from backend.src.models.user import User, UserCreate
from backend.src.services.password_service import hash_password, verify_password, validate_password_strength
from backend.src.core.validators import normalize_email, emails_are_equal


class UserService:
    """Service for user operations"""
    
    @staticmethod
    def check_email_exists(session: Session, email: str) -> bool:
        """
        Check if an email address is already registered (case-insensitive)
        
        Args:
            session: Database session
            email: Email address to check
            
        Returns:
            True if email exists, False otherwise
            
        Example:
            >>> exists = check_email_exists(session, "user@example.com")
            >>> isinstance(exists, bool)
            True
        """
        # Normalize email for case-insensitive comparison
        normalized_email = normalize_email(email)
        if not normalized_email:
            return False
        
        # Query for existing user with normalized email
        statement = select(User).where(User.email == normalized_email.lower())
        result = session.exec(statement)
        user = result.first()
        
        return user is not None
    
    @staticmethod
    def get_user_by_email(session: Session, email: str) -> Optional[User]:
        """
        Get a user by email address (case-insensitive)
        
        Args:
            session: Database session
            email: Email address to look up
            
        Returns:
            User object if found, None otherwise
            
        Example:
            >>> user = get_user_by_email(session, "user@example.com")
            >>> if user:
            ...     print(f"Found user: {user.email}")
        """
        # Normalize email for case-insensitive comparison
        normalized_email = normalize_email(email)
        if not normalized_email:
            return None
        
        # Query for user
        statement = select(User).where(User.email == normalized_email.lower())
        result = session.exec(statement)
        return result.first()
    
    @staticmethod
    def get_user_by_id(session: Session, user_id: UUID) -> Optional[User]:
        """
        Get a user by ID
        
        Args:
            session: Database session
            user_id: User's unique identifier
            
        Returns:
            User object if found, None otherwise
        """
        statement = select(User).where(User.id == user_id)
        result = session.exec(statement)
        return result.first()
    
    @staticmethod
    def create_user(session: Session, user_data: UserCreate) -> User:
        """
        Create a new user account
        
        Args:
            session: Database session
            user_data: User creation data (email, password)
            
        Returns:
            Created User object
            
        Raises:
            ValueError: If email already exists or password is weak
            
        Example:
            >>> user_data = UserCreate(email="user@example.com", password="SecureP@ss123")
            >>> user = create_user(session, user_data)
            >>> user.email == "user@example.com"
            True
        """
        # Validate password strength
        is_valid, error = validate_password_strength(user_data.password)
        if not is_valid:
            raise ValueError(f"Password validation failed: {error}")
        
        # Check for duplicate email (case-insensitive)
        if UserService.check_email_exists(session, user_data.email):
            raise ValueError("Email already registered")
        
        # Normalize email
        normalized_email = normalize_email(user_data.email)
        if not normalized_email:
            raise ValueError("Invalid email format")
        
        # Hash password
        hashed_password = hash_password(user_data.password)
        
        # Create user object
        user = User(
            email=normalized_email.lower(),
            hashed_password=hashed_password,
            is_active=True,
        )
        
        # Add to session and commit
        session.add(user)
        session.commit()
        session.refresh(user)
        
        return user
    
    @staticmethod
    def authenticate_user(
        session: Session,
        email: str,
        password: str
    ) -> Optional[User]:
        """
        Authenticate a user with email and password
        
        Args:
            session: Database session
            email: User's email address
            password: User's password
            
        Returns:
            User object if authentication successful, None otherwise
            
        Example:
            >>> user = authenticate_user(session, "user@example.com", "SecureP@ss123")
            >>> if user:
            ...     print(f"Authenticated: {user.email}")
        """
        # Get user by email
        user = UserService.get_user_by_email(session, email)
        if not user:
            return None
        
        # Check if user is active
        if not user.is_active:
            return None
        
        # Verify password
        password_valid = verify_password(password, user.hashed_password)
        if not password_valid:
            return None
        
        return user
    
    @staticmethod
    def deactivate_user(session: Session, user_id: UUID) -> bool:
        """
        Deactivate a user account (soft delete)
        
        Args:
            session: Database session
            user_id: User's unique identifier
            
        Returns:
            True if successful, False if user not found
        """
        user = UserService.get_user_by_id(session, user_id)
        if not user:
            return False
        
        user.is_active = False
        user.updated_at = datetime.utcnow()
        
        session.add(user)
        session.commit()
        
        return True
