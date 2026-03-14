"""
Task endpoints for CRUD operations
All endpoints require authentication and enforce user isolation
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List

from app.database import get_session
from app.api.deps import get_current_user
from app.models.user import User
from app.models.task import Task, TaskStatus
from app.schemas.task import TaskCreate, TaskRead, TaskUpdate
from app.core.exceptions import ErrorCodes, create_http_exception


router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("", response_model=List[TaskRead])
async def get_tasks(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
) -> List[Task]:
    """
    Get all tasks for the current user
    Returns only tasks owned by the authenticated user
    """
    tasks = session.exec(
        select(Task).where(Task.user_id == current_user.id)
    ).all()
    
    return tasks


@router.post("", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
) -> Task:
    """
    Create a new task for the current user
    """
    task = Task(
        **task_data.dict(),
        user_id=current_user.id
    )
    
    session.add(task)
    session.commit()
    session.refresh(task)
    
    return task


@router.get("/{task_id}", response_model=TaskRead)
async def get_task(
    task_id: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
) -> Task:
    """
    Get a specific task by ID
    Returns 404 if task doesn't exist or doesn't belong to current user
    """
    task = session.exec(
        select(Task).where(
            (Task.id == task_id) & (Task.user_id == current_user.id)
        )
    ).first()
    
    if not task:
        raise create_http_exception(
            detail="Task not found or access denied",
            status_code=status.HTTP_404_NOT_FOUND,
            error_code=ErrorCodes.RESOURCE_NOT_FOUND
        )
    
    return task


@router.put("/{task_id}", response_model=TaskRead)
async def update_task(
    task_id: str,
    task_data: TaskUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
) -> Task:
    """
    Update a task
    Only the task owner can update it
    """
    task = session.exec(
        select(Task).where(
            (Task.id == task_id) & (Task.user_id == current_user.id)
        )
    ).first()
    
    if not task:
        raise create_http_exception(
            detail="Task not found or access denied",
            status_code=status.HTTP_404_NOT_FOUND,
            error_code=ErrorCodes.RESOURCE_NOT_FOUND
        )
    
    # Update only provided fields
    update_data = task_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(task, key, value)
    
    session.add(task)
    session.commit()
    session.refresh(task)
    
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
) -> None:
    """
    Delete a task
    Only the task owner can delete it
    """
    task = session.exec(
        select(Task).where(
            (Task.id == task_id) & (Task.user_id == current_user.id)
        )
    ).first()
    
    if not task:
        raise create_http_exception(
            detail="Task not found or access denied",
            status_code=status.HTTP_404_NOT_FOUND,
            error_code=ErrorCodes.RESOURCE_NOT_FOUND
        )
    
    session.delete(task)
    session.commit()
