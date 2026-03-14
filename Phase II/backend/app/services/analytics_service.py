"""
Analytics Service for Productivity Tracking
Roman Urdu: Analytics Service - Productivity metrics calculate aur update karta hai

Features:
- update_analytics_on_task_create(): Task create hone par analytics update karta hai
- update_analytics_on_task_complete(): Task complete hone par streak recalculate karta hai
- calculate_streak(): Consecutive days with task completion calculate karta hai
- get_category_breakdown(): Category-wise completion rate calculate karta hai

Roman Urdu Comments:
- Yeh service daily productivity metrics track karta hai
- Streak calculation: Lagatar kitne din tasks complete hue
- Category breakdown: Har category mein completion rate
"""

from sqlalchemy.orm import Session
from sqlalchemy import func, extract, and_
from datetime import datetime, date, timedelta
from typing import List, Dict, Optional

from app.models import Analytics, Todo, Category, User


def get_or_create_analytics(
    db: Session,
    user_id: int,
    analytics_date: date
) -> Analytics:
    """
    Get existing analytics record or create new one for the date
    
    Roman Urdu: Date ke liye existing analytics record obtain karna ya naya create karna
    
    Args:
        db: Database session
        user_id: User ka ID
        analytics_date: Date jiske liye analytics chahiye
    
    Returns:
        Analytics record for the date
    """
    # Find existing record
    # Roman Urdu: Existing record dhundhna
    analytics = db.query(Analytics).filter(
        Analytics.user_id == user_id,
        func.date(Analytics.date) == analytics_date
    ).first()
    
    if analytics:
        return analytics
    
    # Create new record
    # Roman Urdu: Naya record create karna
    analytics = Analytics(
        user_id=user_id,
        date=datetime.combine(analytics_date, datetime.min.time()),
        total=0,
        completed=0,
        pending=0,
        streak=0,
        created_at=datetime.utcnow()
    )
    
    db.add(analytics)
    db.commit()
    db.refresh(analytics)
    
    return analytics


def update_analytics_on_task_create(
    db: Session,
    user_id: int,
    task_date: datetime
) -> None:
    """
    Update analytics when a new task is created
    
    Roman Urdu: Jab naya task create hota hai toh analytics update karna
    
    Args:
        db: Database session
        user_id: User ka ID
        task_date: Task ki creation date
    """
    # Get or create analytics for today
    # Roman Urdu: Aaj ke din ke liye analytics obtain ya create karna
    today = date.today()
    analytics = get_or_create_analytics(db, user_id, today)
    
    # Increment total count
    # Roman Urdu: Total count increment karna
    analytics.total += 1
    analytics.pending += 1
    analytics.updated_at = datetime.utcnow()
    
    db.commit()


def update_analytics_on_task_complete(
    db: Session,
    user_id: int,
    completed_date: datetime
) -> None:
    """
    Update analytics when a task is completed
    
    Roman Urdu: Jab task complete hota hai toh analytics update karna aur streak recalculate karna
    
    Args:
        db: Database session
        user_id: User ka ID
        completed_date: Task completion date
    """
    # Get or create analytics for today
    # Roman Urdu: Aaj ke din ke liye analytics obtain ya create karna
    today = date.today()
    analytics = get_or_create_analytics(db, user_id, today)
    
    # Increment completed count, decrement pending
    # Roman Urdu: Completed count increment aur pending decrement karna
    analytics.completed += 1
    if analytics.pending > 0:
        analytics.pending -= 1
    
    # Recalculate streak
    # Roman Urdu: Streak recalculate karna
    analytics.streak = calculate_streak(db, user_id)
    analytics.updated_at = datetime.utcnow()
    
    db.commit()


def update_analytics_on_task_delete(
    db: Session,
    user_id: int,
    task_status: str,
    task_date: datetime
) -> None:
    """
    Update analytics when a task is deleted
    
    Roman Urdu: Jab task delete hota hai toh analytics update karna
    
    Args:
        db: Database session
        user_id: User ka ID
        task_status: Task ka status (pending/completed)
        task_date: Task ki date
    """
    today = date.today()
    analytics = get_or_create_analytics(db, user_id, today)
    
    # Decrement appropriate count
    # Roman Urdu: Appropriate count decrement karna
    analytics.total = max(0, analytics.total - 1)
    
    if task_status == "completed":
        analytics.completed = max(0, analytics.completed - 1)
    else:
        analytics.pending = max(0, analytics.pending - 1)
    
    analytics.updated_at = datetime.utcnow()
    db.commit()


def calculate_streak(
    db: Session,
    user_id: int,
    from_date: Optional[date] = None
) -> int:
    """
    Calculate current completion streak
    
    Roman Urdu: Current completion streak calculate karna - lagatar kitne din tasks complete hue
    
    Args:
        db: Database session
        user_id: User ka ID
        from_date: Date jisse count shuru karna (default: today)
    
    Returns:
        Streak count (consecutive days with at least one completion)
    
    Algorithm:
        1. Start from today (or from_date)
        2. Check if any task was completed on this date
        3. If yes, increment streak and go to previous day
        4. If no, stop - streak broken
        5. Continue until no completion found
    """
    if from_date is None:
        from_date = date.today()
    
    streak = 0
    current_date = from_date
    
    while True:
        # Count completed tasks on this date
        # Roman Urdu: Is date par completed tasks ginti karna
        completed_count = db.query(Todo).filter(
            Todo.user_id == user_id,
            Todo.status == "completed",
            func.date(Todo.completed_at) == current_date
        ).count()
        
        if completed_count > 0:
            # Task completed on this date, continue streak
            # Roman Urdu: Is date par task complete hua, streak jaari rakhta hai
            streak += 1
            current_date -= timedelta(days=1)
        else:
            # No completion, streak broken
            # Roman Urdu: Koi completion nahi, streak toot gaya
            break
        
        # Safety limit: max 365 days
        # Roman Urdu: Safety limit: zyada se zyada 365 din
        if streak >= 365:
            break
    
    return streak


def get_longest_streak(
    db: Session,
    user_id: int,
    from_date: Optional[date] = None,
    lookback_days: int = 365
) -> int:
    """
    Calculate longest streak in a time period
    
    Roman Urdu: Time period mein sabse lamba streak calculate karna
    
    Args:
        db: Database session
        user_id: User ka ID
        from_date: End date (default: today)
        lookback_days: Kitne din peeche tak dekhna hai
    
    Returns:
        Longest streak count in the period
    """
    if from_date is None:
        from_date = date.today()
    
    start_date = from_date - timedelta(days=lookback_days)
    longest = 0
    current_streak = 0
    
    current_date = start_date
    while current_date <= from_date:
        # Check if any task completed on this date
        # Roman Urdu: Check karna ki is date par koi task complete hua
        completed_count = db.query(Todo).filter(
            Todo.user_id == user_id,
            Todo.status == "completed",
            func.date(Todo.completed_at) == current_date
        ).count()
        
        if completed_count > 0:
            current_streak += 1
            longest = max(longest, current_streak)
        else:
            current_streak = 0
        
        current_date += timedelta(days=1)
    
    return longest


def get_category_breakdown(
    db: Session,
    user_id: int,
    limit: int = 10
) -> List[Dict]:
    """
    Get task completion breakdown by category
    
    Roman Urdu: Category ke hisaab se task completion ka breakdown
    
    Args:
        db: Database session
        user_id: User ka ID
        limit: Maximum categories to return
    
    Returns:
        List of category breakdown:
        [
            {
                "category_id": 1,
                "category_name": "Work",
                "category_color": "#4f46e5",
                "total": 10,
                "completed": 7,
                "pending": 3,
                "completion_rate": 70.0
            },
            ...
        ]
    """
    # Query categories with task counts
    # Roman Urdu: Categories ko task counts ke saath query karna
    categories = db.query(
        Category.id,
        Category.name,
        Category.color,
        func.count(Todo.id).label("total"),
        func.sum(case=(Todo.status == "completed", 1), else_=0).label("completed")
    ).outerjoin(
        Todo,
        and_(
            Category.id == Todo.category_id,
            Todo.user_id == user_id,
            Todo.is_deleted == False
        )
    ).filter(
        Category.user_id == user_id
    ).group_by(
        Category.id,
        Category.name,
        Category.color
    ).order_by(
        func.count(Todo.id).desc()
    ).limit(limit).all()
    
    result = []
    for cat in categories:
        total = cat.total or 0
        completed = cat.completed or 0
        pending = total - completed
        completion_rate = (completed / total * 100) if total > 0 else 0.0
        
        result.append({
            "category_id": cat.id,
            "category_name": cat.name,
            "category_color": cat.color,
            "total": total,
            "completed": completed,
            "pending": pending,
            "completion_rate": completion_rate
        })
    
    return result


def get_weekly_trends(
    db: Session,
    user_id: int,
    weeks: int = 4
) -> List[Dict]:
    """
    Get weekly productivity trends
    
    Roman Urdu: Hafta-wise productivity trends obtain karna
    
    Args:
        db: Database session
        user_id: User ka ID
        weeks: Kitne hafton ka data chahiye
    
    Returns:
        List of weekly trends with completion rates
    """
    from sqlalchemy import case
    
    today = date.today()
    trends = []
    
    for i in range(weeks):
        # Calculate week start and end
        # Roman Urdu: Hafta ki shuruat aur ant calculate karna
        week_end = today - timedelta(weeks=i)
        week_start = week_end - timedelta(days=6)
        
        # Get stats for this week
        # Roman Urdu: Is haftay ke stats obtain karna
        stats = db.query(
            func.count(Todo.id).label("total"),
            func.sum(case=(Todo.status == "completed", 1), else_=0).label("completed")
        ).filter(
            Todo.user_id == user_id,
            Todo.is_deleted == False,
            func.date(Todo.created_at) >= week_start,
            func.date(Todo.created_at) <= week_end
        ).first()
        
        total = stats.total or 0
        completed = stats.completed or 0
        pending = total - completed
        completion_rate = (completed / total * 100) if total > 0 else 0.0
        
        trends.append({
            "week_start": week_start.isoformat(),
            "week_end": week_end.isoformat(),
            "total": total,
            "completed": completed,
            "pending": pending,
            "completion_rate": completion_rate
        })
    
    return list(reversed(trends))  # Oldest first


# Helper for SQLAlchemy case statement
def case(conditions, else_=None):
    """Helper for SQLAlchemy case statements"""
    from sqlalchemy import case as sa_case
    return sa_case(conditions, else_=else_)
