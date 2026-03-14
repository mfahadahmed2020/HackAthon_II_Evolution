"""
Task schemas for request/response validation
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class TaskStatus(str, Enum):
    """Task status values"""
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class TaskCreate(BaseModel):
    """
    Schema for task creation request
    """
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.TODO


class TaskRead(BaseModel):
    """
    Schema for task response
    """
    id: str
    user_id: str
    title: str
    description: Optional[str]
    status: TaskStatus
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class TaskUpdate(BaseModel):
    """
    Schema for task update request
    All fields are optional
    """
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
