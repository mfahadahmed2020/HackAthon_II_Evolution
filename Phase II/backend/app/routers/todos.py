from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from datetime import datetime
from ..database import get_db
from app.models import Todo, User, Category
from ..schemas import (
    TodoCreate,
    TodoUpdate,
    TodoResponse,
    TodoListResponse,
    TodoStats,
    RecurringTaskCreate,
    RecurringTaskResponse,
)
from ..auth import get_current_user
from ..utils.recurrence import generate_recurring_instances
from ..websocket import manager
from ..services.analytics_service import (
    update_analytics_on_task_create,
    update_analytics_on_task_complete,
    update_analytics_on_task_delete,
)

router = APIRouter()

# ============ Create Todo ============

@router.post("/todos", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
async def create_todo(
    todo_data: TodoCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new todo
    
    Roman Urdu: Naya task create karna with optional category assignment
    """
    # Phase 2: Validate category_id if provided
    # Roman Urdu: Agar category_id diya gaya hai toh validate karna
    if todo_data.category_id is not None:
        category = db.query(Category).filter(
            Category.id == todo_data.category_id,
            Category.user_id == current_user.id
        ).first()
        if not category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid category_id - Category not found or you don't have permission"
            )
    
    new_todo = Todo(
        title=todo_data.title,
        description=todo_data.description,
        priority=todo_data.priority,
        due_date=todo_data.due_date,
        user_id=current_user.id,
        category_id=todo_data.category_id  # Phase 2: Category support
    )

    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    
    # Phase 6: Update analytics
    # Roman Urdu: Analytics update karna jab task create hota hai
    update_analytics_on_task_create(db, current_user.id, new_todo.created_at)
    
    # Phase 5: Broadcast to user via WebSocket
    # Roman Urdu: WebSocket ke zariye user ko broadcast karna
    await manager.broadcast_to_user(
        current_user.id,
        {
            "type": "task.created",
            "data": {
                "id": new_todo.id,
                "title": new_todo.title,
                "status": new_todo.status
            }
        }
    )

    return new_todo


# ============ Create Recurring Task ============
# Phase 2: Recurring Tasks - Bulk Generation

@router.post(
    "/todos/recurring",
    response_model=RecurringTaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create recurring task",
    description="Recurring task create karein - saare future occurrences ek saath generate honge",
    response_description="Created recurring tasks with parent_id and count",
)
async def create_recurring_task(
    recurring_task: RecurringTaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create a recurring task with all occurrences generated at once
    
    Roman Urdu: Ek recurring task create karta hai aur saare future instances ek saath generate karta hai.
    User ek baar request bhejta hai aur multiple tasks ek saath create ho jate hain.
    
    **Example:**
    ```json
    {
        "title": "Daily standup",
        "description": "Team sync meeting",
        "priority": "high",
        "recurrence_pattern": "daily",
        "occurrences": 30,
        "start_date": "2026-03-11T09:00:00Z",
        "category_id": 1
    }
    ```
    
    **Response:**
    - parent_id: Parent task ka ID (first occurrence)
    - created_count: Kitne tasks create hue
    - tasks: Saare created tasks ki list
    
    **Validation:**
    - recurrence_pattern: daily, weekly, ya monthly hona chahiye
    - occurrences: 1-365 ke beech hona chahiye
    - start_date: Valid datetime hona chahiye
    
    **Roman Urdu Comments:**
    - Yeh endpoint ek parent task create karta hai
    - Phir saare child instances (occurrences) create hote hain
    - Pehla instance parent task banta hai
    - Baaki instances uske children hote hain
    """
    # Validate category_id if provided
    # Roman Urdu: Agar category_id diya gaya hai toh validate karna
    if recurring_task.category_id is not None:
        category = db.query(Category).filter(
            Category.id == recurring_task.category_id,
            Category.user_id == current_user.id
        ).first()
        if not category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid category_id - Category not found or you don't have permission"
            )
    
    # Generate all occurrences using utility
    # Roman Urdu: Saare occurrences generate karna using utility function
    instances = generate_recurring_instances(
        start_date=recurring_task.start_date,
        recurrence_pattern=recurring_task.recurrence_pattern,
        occurrences=recurring_task.occurrences,
        title=recurring_task.title,
        description=recurring_task.description,
        priority=recurring_task.priority,
        category_id=recurring_task.category_id
    )
    
    # Create all tasks in a single database transaction
    # Roman Urdu: Saare tasks ek hi database transaction mein create karna
    created_tasks = []
    parent_id = None
    
    try:
        for i, instance_data in enumerate(instances):
            # Create task instance
            # Roman Urdu: Task instance create karna
            todo = Todo(
                title=instance_data["title"],
                description=instance_data["description"],
                priority=instance_data["priority"],
                due_date=instance_data["due_date"],
                user_id=current_user.id,
                category_id=instance_data["category_id"],
                recurrence_pattern=instance_data["recurrence_pattern"],
                status=instance_data["status"],
                is_deleted=instance_data["is_deleted"]
            )
            
            # First task is the parent
            # Roman Urdu: Pehla task parent hota hai
            if i == 0:
                parent_id = todo.id  # Will be set after flush
            
            db.add(todo)
            created_tasks.append(todo)
        
        # Flush to get IDs
        # Roman Urdu: IDs obtain karne ke liye flush karna
        db.flush()
        
        # Set parent_id for all tasks
        # Roman Urdu: Saare tasks mein parent_id set karna
        for i, todo in enumerate(created_tasks):
            if i == 0:
                parent_id = todo.id
                todo.parent_id = None  # Parent ka parent NULL
            else:
                todo.parent_id = parent_id
        
        # Commit transaction
        # Roman Urdu: Transaction commit karna
        db.commit()
        
        # Refresh all tasks to get complete data
        # Roman Urdu: Saare tasks ko refresh karna complete data ke liye
        for todo in created_tasks:
            db.refresh(todo)
        
        return RecurringTaskResponse(
            parent_id=parent_id,
            created_count=len(created_tasks),
            tasks=created_tasks
        )
    
    except Exception as e:
        # Rollback on error
        # Roman Urdu: Error par rollback karna
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create recurring tasks: {str(e)}"
        )


# ============ Get All Todos ============

@router.get("/todos", response_model=TodoListResponse)
async def get_todos(
    status_filter: Optional[str] = Query(None, alias="status_filter", pattern="^(pending|completed)$"),
    priority: Optional[str] = Query(None, pattern="^(low|medium|high)$"),
    category_id: Optional[int] = Query(None, description="Filter by category ID"),
    sort: str = Query("created_at"),
    order: str = Query("desc"),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all todos with filters, search, and pagination
    
    Roman Urdu: Category filter support - tasks ko category se filter kar sakte hain
    """
    # Base query - only user's non-deleted todos
    # Use joinedload to eagerly load category data
    query = db.query(Todo).options(
        joinedload(Todo.category)
    ).filter(
        Todo.user_id == current_user.id,
        Todo.is_deleted == False
    )

    # Apply filters
    if status_filter:
        query = query.filter(Todo.status == status_filter)
    if priority:
        query = query.filter(Todo.priority == priority)
    # Phase 2: Category filter
    # Roman Urdu: Category ID se filter karna
    if category_id is not None:
        query = query.filter(Todo.category_id == category_id)
    if search:
        query = query.filter(
            (Todo.title.contains(search)) | (Todo.description.contains(search))
        )

    # Get total count before pagination
    total = query.count()

    # Apply sorting
    sort_column = getattr(Todo, sort, Todo.created_at)
    if order == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())

    # Apply pagination
    offset = (page - 1) * limit
    todos = query.offset(offset).limit(limit).all()

    return TodoListResponse(
        todos=todos,
        total=total,
        page=page,
        limit=limit
    )

# ============ Get Single Todo ============

@router.get("/todos/{todo_id}", response_model=TodoResponse)
async def get_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a single todo by ID"""
    todo = db.query(Todo).options(
        joinedload(Todo.category)
    ).filter(
        Todo.id == todo_id,
        Todo.user_id == current_user.id,
        Todo.is_deleted == False
    ).first()

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    return todo

# ============ Update Todo ============

@router.put("/todos/{todo_id}", response_model=TodoResponse)
async def update_todo(
    todo_id: int,
    todo_data: TodoUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a todo"""
    todo = db.query(Todo).options(
        joinedload(Todo.category)
    ).filter(
        Todo.id == todo_id,
        Todo.user_id == current_user.id,
        Todo.is_deleted == False
    ).first()

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    # Update fields
    update_data = todo_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(todo, field, value)

    todo.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(todo)
    
    # Phase 5: Broadcast to user via WebSocket
    # Roman Urdu: WebSocket ke zariye user ko broadcast karna
    await manager.broadcast_to_user(
        current_user.id,
        {
            "type": "task.updated",
            "data": {
                "id": todo.id,
                "title": todo.title,
                "status": todo.status,
                "priority": todo.priority
            }
        }
    )

    return todo

# ============ Delete Todo (Soft Delete) ============

@router.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Soft delete a todo"""
    todo = db.query(Todo).filter(
        Todo.id == todo_id,
        Todo.user_id == current_user.id,
        Todo.is_deleted == False
    ).first()
    
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    
    todo.is_deleted = True
    todo.deleted_at = datetime.utcnow()
    db.commit()
    
    # Phase 6: Update analytics
    # Roman Urdu: Analytics update karna jab task delete hota hai
    update_analytics_on_task_delete(db, current_user.id, todo.status, todo.created_at)

    # Phase 5: Broadcast to user via WebSocket
    # Roman Urdu: WebSocket ke zariye user ko broadcast karna
    await manager.broadcast_to_user(
        current_user.id,
        {
            "type": "task.deleted",
            "data": {
                "id": todo_id
            }
        }
    )

    return None

# ============ Mark as Complete ============

@router.patch("/todos/{todo_id}/complete", response_model=TodoResponse)
async def mark_complete(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Mark a todo as completed"""
    todo = db.query(Todo).options(
        joinedload(Todo.category)
    ).filter(
        Todo.id == todo_id,
        Todo.user_id == current_user.id,
        Todo.is_deleted == False
    ).first()

    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    todo.status = "completed"
    todo.completed_at = datetime.utcnow()
    todo.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(todo)
    
    # Phase 6: Update analytics
    # Roman Urdu: Analytics update karna jab task complete hota hai
    update_analytics_on_task_complete(db, current_user.id, todo.completed_at)
    
    # Phase 5: Broadcast to user via WebSocket
    # Roman Urdu: WebSocket ke zariye user ko broadcast karna
    await manager.broadcast_to_user(
        current_user.id,
        {
            "type": "task.updated",
            "data": {
                "id": todo.id,
                "title": todo.title,
                "status": "completed",
                "completed_at": todo.completed_at.isoformat() if todo.completed_at else None
            }
        }
    )

    return todo

# ============ Mark as Pending ============

@router.patch("/todos/{todo_id}/pending", response_model=TodoResponse)
async def mark_pending(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Mark a todo as pending"""
    todo = db.query(Todo).options(
        joinedload(Todo.category)
    ).filter(
        Todo.id == todo_id,
        Todo.user_id == current_user.id,
        Todo.is_deleted == False
    ).first()

    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    todo.status = "pending"
    todo.completed_at = None
    todo.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(todo)

    return todo

# ============ Toggle Status ============

@router.patch("/todos/{todo_id}/toggle", response_model=TodoResponse)
async def toggle_status(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Toggle todo status between pending and completed"""
    todo = db.query(Todo).options(
        joinedload(Todo.category)
    ).filter(
        Todo.id == todo_id,
        Todo.user_id == current_user.id,
        Todo.is_deleted == False
    ).first()

    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    if todo.status == "pending":
        todo.status = "completed"
        todo.completed_at = datetime.utcnow()
    else:
        todo.status = "pending"
        todo.completed_at = None

    todo.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(todo)

    return todo

# ============ Search Todos ============

@router.get("/todos/search", response_model=List[TodoResponse])
async def search_todos(
    q: str = Query(..., min_length=1),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Search todos by title or description"""
    todos = db.query(Todo).options(
        joinedload(Todo.category)
    ).filter(
        Todo.user_id == current_user.id,
        Todo.is_deleted == False,
        (Todo.title.contains(q)) | (Todo.description.contains(q))
    ).all()

    return todos

# ============ Get Statistics ============

@router.get("/todos/stats", response_model=TodoStats)
async def get_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get todo statistics"""
    base_query = db.query(Todo).filter(
        Todo.user_id == current_user.id,
        Todo.is_deleted == False
    )
    
    total = base_query.count()
    completed = base_query.filter(Todo.status == "completed").count()
    pending = base_query.filter(Todo.status == "pending").count()
    
    completion_percentage = (completed / total * 100) if total > 0 else 0.0
    
    return TodoStats(
        total=total,
        completed=completed,
        pending=pending,
        completion_percentage=completion_percentage
    )
