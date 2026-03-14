"""
Category Management API Router
Roman Urdu: Category CRUD operations - users apne tasks ko organize karne ke liye categories bana sakte hain

Features:
- POST /api/categories - Naya category create karein
- GET /api/categories - Saare categories list karein (current user ke)
- PUT /api/categories/{category_id} - Category update karein
- DELETE /api/categories/{category_id} - Category delete karein (soft delete)

Error Messages (Roman Urdu):
- "Category pehle se मौजूद hai" - Duplicate category name
- "Category nahi mili" - Category not found
- "Aap is category ko edit nahi kar sakte" - Not owner
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.database import get_db
from app.auth import get_current_user
from app.models import User, Category, Todo
from app.schemas import (
    CategoryCreate,
    CategoryUpdate,
    CategoryResponse,
    CategoryListResponse,
)


router = APIRouter(
    prefix="/categories",
    tags=["categories"],
    dependencies=[Depends(get_current_user)],
    responses={
        401: {"description": "Unauthorized - Token invalid ya expire ho gaya"},
        403: {"description": "Forbidden - Aap is action ko perform nahi kar sakte"},
        404: {"description": "Not Found - Category nahi mili"},
    },
)


@router.post(
    "",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create new category",
    description="Naya category create karein - tasks ko organize karne ke liye",
    response_description="Created category ka details",
)
async def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Naya category create karein
    
    Roman Urdu: User apne tasks ko organize karne ke liye naya category bana sakta hai.
    Category name aur color specify karna hota hai. Color hex code format mein hona chahiye (#RRGGBB).
    
    **Example:**
    ```json
    {
        "name": "Work",
        "color": "#4f46e5"
    }
    ```
    
    **Error Cases:**
    - Category pehle se मौजूद hai (same name ka category already exists)
    - Invalid color format (hex code nahi hai)
    """
    # Check if category with same name already exists for this user
    # Roman Urdu: Check karna ki same name ka category pehle se toh nahi hai
    existing_category = db.query(Category).filter(
        Category.user_id == current_user.id,
        Category.name.ilike(category.name)  # Case-insensitive comparison
    ).first()
    
    if existing_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category pehle se मौजूद hai - Same name ka category already exists"
        )
    
    # Create new category
    # Roman Urdu: Naya category create karna
    db_category = Category(
        user_id=current_user.id,
        name=category.name,
        color=category.color,
        created_at=datetime.utcnow()
    )
    
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    
    return db_category


@router.get(
    "",
    response_model=CategoryListResponse,
    status_code=status.HTTP_200_OK,
    summary="List all categories",
    description="Current user ke saare categories list karein",
    response_description="Categories ki list with total count",
)
async def list_categories(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Current user ke saare categories retrieve karein
    
    Roman Urdu: User ke saare categories ko created_at ke order mein return karta hai.
    Categories tasks ko organize karne mein help karte hain.
    
    **Response:**
    - categories: Categories ki list
    - total: Total categories count
    """
    # Get all categories for current user
    # Roman Urdu: Current user ke saare categories fetch karna
    categories = db.query(Category).filter(
        Category.user_id == current_user.id
    ).order_by(Category.created_at.asc()).all()
    
    return CategoryListResponse(
        categories=categories,
        total=len(categories)
    )


@router.get(
    "/{category_id}",
    response_model=CategoryResponse,
    status_code=status.HTTP_200_OK,
    summary="Get category details",
    description="Specific category ka details retrieve karein",
    response_description="Category details",
)
async def get_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Specific category ka details retrieve karein
    
    Roman Urdu: Category ID se category ka details fetch karta hai.
    Sirf owner hi apne category ko dekh sakta hai.
    
    **Error Cases:**
    - Category nahi mili (404)
    - Aap is category ko dekh nahi sakte (403 - not owner)
    """
    # Find category by ID
    # Roman Urdu: Category ID se category dhundhna
    category = db.query(Category).filter(
        Category.id == category_id
    ).first()
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category nahi mili - Category not found"
        )
    
    # Check ownership
    # Roman Urdu: Check karna ki yeh user ka category hai ya nahi
    if category.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Aap is category ko dekh nahi sakte - You are not the owner"
        )
    
    return category


@router.put(
    "/{category_id}",
    response_model=CategoryResponse,
    status_code=status.HTTP_200_OK,
    summary="Update category",
    description="Category ka details update karein (name ya color)",
    response_description="Updated category details",
)
async def update_category(
    category_id: int,
    category_update: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Category ka details update karein
    
    Roman Urdu: Category ka naam ya color update kiya ja sakta hai.
    Sirf owner hi apne category ko update kar sakta hai.
    
    **Example:**
    ```json
    {
        "name": "Personal Work",
        "color": "#10b981"
    }
    ```
    
    **Error Cases:**
    - Category nahi mili (404)
    - Aap is category ko edit nahi kar sakte (403 - not owner)
    - Category pehle se मौजूद hai (duplicate name)
    """
    # Find category by ID
    # Roman Urdu: Category ID se category dhundhna
    category = db.query(Category).filter(
        Category.id == category_id
    ).first()
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category nahi mili - Category not found"
        )
    
    # Check ownership
    # Roman Urdu: Check karna ki yeh user ka category hai ya nahi
    if category.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Aap is category ko edit nahi kar sakte - You are not the owner"
        )
    
    # Check for duplicate name if name is being updated
    # Roman Urdu: Agar name update ho raha hai toh duplicate check karna
    if category_update.name is not None:
        existing_category = db.query(Category).filter(
            Category.user_id == current_user.id,
            Category.name.ilike(category_update.name),
            Category.id != category_id  # Exclude current category
        ).first()
        
        if existing_category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category pehle se मौजूद hai - Same name ka category already exists"
            )
    
    # Update category fields
    # Roman Urdu: Category fields update karna
    update_data = category_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(category, field, value)
    
    category.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(category)
    
    return category


@router.delete(
    "/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete category",
    description="Category ko delete karein (soft delete)",
    response_description="No content - Successfully deleted",
)
async def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Category ko delete karein
    
    Roman Urdu: Category ko permanently delete nahi kiya jata, balki soft delete kiya jata hai.
    Is category se jude saare tasks mein se category_id NULL set ho jata hai.
    
    **Important:**
    - Category permanently delete ho jata hai
    - Is category se jude saare tasks mein category_id = NULL set ho jata hai
    - Yeh action reversible nahi hai
    
    **Error Cases:**
    - Category nahi mili (404)
    - Aap is category ko delete nahi kar sakte (403 - not owner)
    """
    # Find category by ID
    # Roman Urdu: Category ID se category dhundhna
    category = db.query(Category).filter(
        Category.id == category_id
    ).first()
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category nahi mili - Category not found"
        )
    
    # Check ownership
    # Roman Urdu: Check karna ki yeh user ka category hai ya nahi
    if category.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Aap is category ko delete nahi kar sakte - You are not the owner"
        )
    
    # Set category_id to NULL for all tasks in this category
    # Roman Urdu: Is category se jude saare tasks mein category_id NULL set karna
    db.query(Todo).filter(
        Todo.category_id == category_id
    ).update({"category_id": None})
    
    # Delete the category
    # Roman Urdu: Category ko permanently delete karna
    db.delete(category)
    db.commit()
    
    return None
