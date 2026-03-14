from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime, date
from typing import Optional, List
import re

# ============ User Schemas ============

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None

class PasswordChange(BaseModel):
    old_password: str
    new_password: str = Field(..., min_length=6)

# ============ Token Schemas ============

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    exp: Optional[datetime] = None

# ============ Todo Schemas ============

class TodoCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    priority: str = Field(default="medium", pattern="^(low|medium|high|urgent)$")
    due_date: Optional[datetime] = None
    # Phase 2: Category support
    category_id: Optional[int] = None  # Optional category assignment

class TodoUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    priority: Optional[str] = Field(None, pattern="^(low|medium|high|urgent)$")
    due_date: Optional[datetime] = None
    # Phase 2: Category support
    category_id: Optional[int] = None  # Update category assignment

class TodoResponse(BaseModel):
    """
    Todo response schema with Phase 2 extensions
    Roman Urdu: Todo response with category aur recurrence info
    """
    id: int
    user_id: int
    title: str
    description: Optional[str]
    priority: str
    due_date: Optional[datetime]
    status: str
    # Phase 2: Category info
    category_id: Optional[int] = None
    category_name: Optional[str] = None  # For UI convenience (via JOIN)
    category_color: Optional[str] = None  # For UI color badge
    # Phase 2: Recurrence info
    recurrence_pattern: Optional[str] = None
    parent_id: Optional[int] = None
    # Timestamps
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime]

    class Config:
        from_attributes = True

class TodoListResponse(BaseModel):
    todos: List[TodoResponse]
    total: int
    page: int
    limit: int

class TodoStats(BaseModel):
    total: int
    completed: int
    pending: int
    completion_percentage: float


# ============ Phase 2: Category Schemas ============
# Roman Urdu: Category schemas - task organization ke liye

class CategoryCreate(BaseModel):
    """
    Category create karne ke liye schema
    Roman Urdu: Naya category banane ka schema
    """
    name: str = Field(..., min_length=1, max_length=50)
    color: str = Field(default="#6366f1")  # Default indigo color
    
    @field_validator('color')
    @classmethod
    def validate_color(cls, v):
        """
        Validate hex color format
        Roman Urdu: Hex color code validate karna (#RRGGBB)
        """
        if not re.match(r'^#[0-9A-Fa-f]{6}$', v):
            raise ValueError('Color must be a valid hex color code (e.g., #4f46e5)')
        return v

class CategoryUpdate(BaseModel):
    """
    Category update karne ke liye schema
    Roman Urdu: Category update karne ka schema
    """
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    color: Optional[str] = Field(None)
    
    @field_validator('color')
    @classmethod
    def validate_color(cls, v):
        """Validate hex color format"""
        if v is not None and not re.match(r'^#[0-9A-Fa-f]{6}$', v):
            raise ValueError('Color must be a valid hex color code (e.g., #4f46e5)')
        return v

class CategoryResponse(BaseModel):
    """
    Category response schema
    Roman Urdu: Category ka response bhejne ka schema
    """
    id: int
    user_id: int
    name: str
    color: str
    created_at: datetime

    class Config:
        from_attributes = True

class CategoryListResponse(BaseModel):
    """
    Multiple categories return karne ke liye schema
    Roman Urdu: Saare categories list karne ka schema
    """
    categories: List[CategoryResponse]
    total: int


# ============ Phase 2: Analytics Schemas ============
# Roman Urdu: Analytics schemas - productivity tracking ke liye

class AnalyticsStats(BaseModel):
    """
    Current productivity stats
    Roman Urdu: Current productivity metrics
    """
    total: int
    completed: int
    pending: int
    completion_percentage: float
    current_streak: int
    longest_streak: int
    categories_breakdown: Optional[List[dict]] = None

class WeeklyTrend(BaseModel):
    """
    Weekly productivity trend
    Roman Urdu: Hafta-wise productivity trend
    """
    week_start: date
    week_end: date
    total: int
    completed: int
    pending: int
    completion_rate: float

class WeeklyTrendsResponse(BaseModel):
    """
    Multiple weeks trends
    Roman Urdu: Kai hafton ka trend data
    """
    weeks: List[WeeklyTrend]

class MonthlyTrend(BaseModel):
    """
    Monthly productivity trend
    Roman Urdu: Mahina-wise productivity trend
    """
    month: str  # YYYY-MM format
    total: int
    completed: int
    pending: int
    completion_rate: float
    avg_streak: int

class MonthlyTrendsResponse(BaseModel):
    """
    Multiple months trends
    Roman Urdu: Kai mahino ka trend data
    """
    months: List[MonthlyTrend]


# ============ Phase 2: Recurring Task Schemas ============
# Roman Urdu: Recurring task schemas - repeated tasks ke liye

class RecurringTaskCreate(BaseModel):
    """
    Recurring task create karne ke liye schema
    Roman Urdu: Recurring task banane ka schema
    """
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    priority: str = Field(default="medium", pattern="^(low|medium|high|urgent)$")
    recurrence_pattern: str = Field(..., pattern="^(daily|weekly|monthly)$")
    occurrences: int = Field(default=30, ge=1, le=365)  # Min 1, Max 365
    start_date: datetime
    category_id: Optional[int] = None
    
    @field_validator('occurrences')
    @classmethod
    def validate_occurrences(cls, v):
        """
        Validate occurrences count
        Roman Urdu: Occurrences count validate karna (1-365)
        """
        if v < 1:
            raise ValueError('Occurrences must be at least 1')
        if v > 365:
            raise ValueError('Occurrences cannot exceed 365')
        return v

class RecurringTaskResponse(BaseModel):
    """
    Recurring task creation response
    Roman Urdu: Recurring task create karne ka response
    """
    parent_id: int
    created_count: int
    tasks: List[TodoResponse]
