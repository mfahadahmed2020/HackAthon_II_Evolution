from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    """
    User model for authentication
    Roman Urdu: User table - authentication aur profile ke liye
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships - Phase 2 ke saath
    todos = relationship("Todo", back_populates="user", cascade="all, delete-orphan")
    categories = relationship("Category", back_populates="user", cascade="all, delete-orphan")
    analytics = relationship("Analytics", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.username}>"


class Category(Base):
    """
    Category model for task organization
    Roman Urdu: Category table - tasks ko organize karne ke liye
    Phase 2 Feature: User-defined custom categories with color coding
    """
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(50), nullable=False)  # Category name (e.g., "Work", "Personal")
    color = Column(String(7), nullable=False, default="#6366f1")  # Hex color code (#RRGGBB)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship with user
    user = relationship("User", back_populates="categories")
    
    # Relationship with todos - one category can have many tasks
    tasks = relationship("Todo", back_populates="category")

    # Unique constraint: ek user ke liye category name unique hona chahiye
    __table_args__ = (
        UniqueConstraint('user_id', 'name', name='uq_user_category_name'),
    )

    def __repr__(self):
        return f"<Category {self.name} ({self.color})>"


class Analytics(Base):
    """
    Analytics model for productivity tracking
    Roman Urdu: Analytics table - productivity metrics store karne ke liye
    Phase 2 Feature: Daily productivity stats, streaks, trends
    """
    __tablename__ = "analytics"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    date = Column(DateTime, nullable=False)  # Date for these metrics
    total = Column(Integer, nullable=False, default=0)  # Total tasks for this date
    completed = Column(Integer, nullable=False, default=0)  # Completed tasks count
    pending = Column(Integer, nullable=False, default=0)  # Pending tasks count
    streak = Column(Integer, nullable=False, default=0)  # Current completion streak (days)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship with user
    user = relationship("User", back_populates="analytics")

    # Unique constraint: ek user ke liye ek date mein ek record
    __table_args__ = (
        UniqueConstraint('user_id', 'date', name='uq_user_analytics_date'),
    )

    def __repr__(self):
        return f"<Analytics {self.date} - {self.completed}/{self.total}>"


class Todo(Base):
    """
    Todo model for task management
    Roman Urdu: Todo table - tasks manage karne ke liye
    Phase 2 Extensions: Categories, Recurring Tasks, Soft Delete
    """
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    priority = Column(String(10), default="medium")  # low, medium, high, urgent
    due_date = Column(DateTime, nullable=True)
    status = Column(String(10), default="pending")  # pending, completed
    
    # Phase 2: Category support
    # Roman Urdu: Category ID - task ko category se jodta hai
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"), nullable=True, index=True)
    
    # Phase 2: Recurring task support
    # Roman Urdu: Recurrence pattern - daily, weekly, monthly
    recurrence_pattern = Column(String(50), nullable=True)  # daily, weekly, monthly, NULL for non-recurring
    
    # Phase 2: Parent task for recurring instances
    # Roman Urdu: Parent ID - recurring task ka original task
    parent_id = Column(Integer, ForeignKey("todos.id", ondelete="CASCADE"), nullable=True, index=True)
    
    # Phase 2: Soft delete
    # Roman Urdu: Soft delete flag - hard delete ki jagah flag use karte hain
    is_deleted = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    deleted_at = Column(DateTime, nullable=True)

    # Relationships
    user = relationship("User", back_populates="todos")
    
    # Phase 2: Category relationship
    # Roman Urdu: Category relationship - task ka category object
    category = relationship("Category", back_populates="todos")
    
    # Phase 2: Self-referential relationship for recurring tasks
    # Roman Urdu: Parent-child relationship for recurring tasks
    parent = relationship("Todo", remote_side=[id], back_populates="children")
    children = relationship("Todo", remote_side=[parent_id], back_populates="parent")

    def __repr__(self):
        return f"<Todo {self.title}>"
