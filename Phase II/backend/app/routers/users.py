from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from app.models import User
from ..schemas import UserResponse, UserUpdate, PasswordChange
from ..utils.security import hash_password, verify_password
from ..auth import get_current_user

router = APIRouter()

@router.get("/user/profile", response_model=UserResponse)
async def get_profile(
    current_user: User = Depends(get_current_user)
):
    """Get current user profile"""
    return current_user

@router.put("/user/profile", response_model=UserResponse)
async def update_profile(
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update user profile"""
    update_data = user_data.model_dump(exclude_unset=True)
    
    # Check email uniqueness if changing email
    if user_data.email and user_data.email != current_user.email:
        existing = db.query(User).filter(User.email == user_data.email).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
    
    # Check username uniqueness if changing username
    if user_data.username and user_data.username != current_user.username:
        existing = db.query(User).filter(User.username == user_data.username).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
    
    # Update fields
    for field, value in update_data.items():
        setattr(current_user, field, value)
    
    current_user.updated_at = __import__('datetime').datetime.utcnow()
    db.commit()
    db.refresh(current_user)
    
    return current_user

@router.put("/user/password")
async def change_password(
    password_data: PasswordChange,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Change user password"""
    # Verify old password
    if not verify_password(password_data.old_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid current password"
        )
    
    # Update password
    current_user.password_hash = hash_password(password_data.new_password)
    current_user.updated_at = __import__('datetime').datetime.utcnow()
    db.commit()
    
    return {"message": "Password changed successfully"}
