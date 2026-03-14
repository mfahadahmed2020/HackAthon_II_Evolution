"""
Analytics API Router
Roman Urdu: Analytics API - Productivity stats, trends, aur category breakdown

Endpoints:
- GET /api/analytics/stats - Current productivity stats
- GET /api/analytics/weekly - Weekly trends
- GET /api/analytics/monthly - Monthly trends

Roman Urdu Comments:
- Yeh endpoints user ki productivity metrics return karte hain
- Stats mein completion rate, streaks, category breakdown shamil hain
- Trends hafta aur mahina-wise productivity dikhate hain
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date, timedelta

from app.database import get_db
from app.auth import get_current_user
from app.models import User
from app.schemas import (
    AnalyticsStats,
    WeeklyTrendsResponse,
    WeeklyTrend,
    MonthlyTrendsResponse,
    MonthlyTrend,
)
from app.services.analytics_service import (
    calculate_streak,
    get_longest_streak,
    get_category_breakdown,
    get_weekly_trends,
)
from app.websocket import manager

router = APIRouter(
    prefix="/analytics",
    tags=["analytics"],
    dependencies=[Depends(get_current_user)],
    responses={
        401: {"description": "Unauthorized - Token invalid ya expire ho gaya"},
    },
)


@router.get(
    "/stats",
    response_model=AnalyticsStats,
    status_code=status.HTTP_200_OK,
    summary="Get productivity stats",
    description="Current productivity statistics - completion rate, streaks, category breakdown",
    response_description="Productivity stats with breakdowns",
)
async def get_productivity_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get current productivity statistics
    
    Roman Urdu: Current productivity metrics obtain karna
    
    Returns:
        - total: Total tasks count
        - completed: Completed tasks count
        - pending: Pending tasks count
        - completion_percentage: Completion rate percentage
        - current_streak: Current completion streak (days)
        - longest_streak: Longest streak in last 365 days
        - categories_breakdown: Category-wise completion stats
    """
    from sqlalchemy import func
    from app.models import Todo
    
    # Get base stats
    # Roman Urdu: Base stats obtain karna
    base_query = db.query(Todo).filter(
        Todo.user_id == current_user.id,
        Todo.is_deleted == False
    )
    
    total = base_query.count()
    completed = base_query.filter(Todo.status == "completed").count()
    pending = base_query.filter(Todo.status == "pending").count()
    
    completion_percentage = (completed / total * 100) if total > 0 else 0.0
    
    # Calculate streaks
    # Roman Urdu: Streaks calculate karna
    current_streak = calculate_streak(db, current_user.id)
    longest_streak = get_longest_streak(db, current_user.id, lookback_days=365)
    
    # Get category breakdown
    # Roman Urdu: Category breakdown obtain karna
    categories_breakdown = get_category_breakdown(db, current_user.id, limit=10)
    
    return AnalyticsStats(
        total=total,
        completed=completed,
        pending=pending,
        completion_percentage=completion_percentage,
        current_streak=current_streak,
        longest_streak=longest_streak,
        categories_breakdown=categories_breakdown
    )


@router.get(
    "/weekly",
    response_model=WeeklyTrendsResponse,
    status_code=status.HTTP_200_OK,
    summary="Get weekly trends",
    description="Weekly productivity trends - last N weeks",
    response_description="Weekly trends data",
)
async def get_weekly_trends_endpoint(
    weeks: int = Query(default=4, ge=1, le=12, description="Number of weeks (1-12)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get weekly productivity trends
    
    Roman Urdu: Hafta-wise productivity trends obtain karna
    
    Query Parameters:
        weeks: Kitne hafton ka data chahiye (1-12, default 4)
    
    Returns:
        List of weekly trends with:
        - week_start: Haftay ki shuruat
        - week_end: Haftay ka ant
        - total: Total tasks
        - completed: Completed tasks
        - pending: Pending tasks
        - completion_rate: Completion percentage
    """
    trends_data = get_weekly_trends(db, current_user.id, weeks=weeks)
    
    # Convert to response model
    # Roman Urdu: Response model mein convert karna
    weeks_list = [
        WeeklyTrend(
            week_start=t["week_start"],
            week_end=t["week_end"],
            total=t["total"],
            completed=t["completed"],
            pending=t["pending"],
            completion_rate=t["completion_rate"]
        )
        for t in trends_data
    ]
    
    return WeeklyTrendsResponse(weeks=weeks_list)


@router.get(
    "/monthly",
    response_model=MonthlyTrendsResponse,
    status_code=status.HTTP_200_OK,
    summary="Get monthly trends",
    description="Monthly productivity trends - last N months",
    response_description="Monthly trends data",
)
async def get_monthly_trends_endpoint(
    months: int = Query(default=6, ge=1, le=24, description="Number of months (1-24)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get monthly productivity trends
    
    Roman Urdu: Mahina-wise productivity trends obtain karna
    
    Query Parameters:
        months: Kitne mahino ka data chahiye (1-24, default 6)
    
    Returns:
        List of monthly trends with:
        - month: Mahina (YYYY-MM format)
        - total: Total tasks
        - completed: Completed tasks
        - pending: Pending tasks
        - completion_rate: Completion percentage
        - avg_streak: Average streak for the month
    """
    from sqlalchemy import func
    from app.models import Todo
    from datetime import datetime
    
    today = date.today()
    trends = []
    
    for i in range(months):
        # Calculate month
        # Roman Urdu: Mahina calculate karna
        if today.month - i <= 0:
            month_num = 12 + (today.month - i)
            year = today.year - 1
        else:
            month_num = today.month - i
            year = today.year
        
        month_str = f"{year}-{month_num:02d}"
        
        # Get stats for this month
        # Roman Urdu: Is mahine ke stats obtain karna
        month_start = datetime(year, month_num, 1).date()
        if month_num == 12:
            month_end = datetime(year + 1, 1, 1).date() - timedelta(days=1)
        else:
            month_end = datetime(year, month_num + 1, 1).date() - timedelta(days=1)
        
        stats = db.query(Todo).filter(
            Todo.user_id == current_user.id,
            Todo.is_deleted == False,
            func.date(Todo.created_at) >= month_start,
            func.date(Todo.created_at) <= month_end
        ).all()
        
        total = len(stats)
        completed = sum(1 for t in stats if t.status == "completed")
        pending = total - completed
        completion_rate = (completed / total * 100) if total > 0 else 0.0
        
        # Calculate average streak for month
        # Roman Urdu: Mahine ka average streak calculate karna
        month_streaks = []
        for day in range(1, 29):  # Check first 28 days
            check_date = datetime(year, month_num, min(day, 28)).date()
            streak = calculate_streak(db, current_user.id, from_date=check_date)
            month_streaks.append(streak)
        
        avg_streak = sum(month_streaks) / len(month_streaks) if month_streaks else 0
        
        trends.append({
            "month": month_str,
            "total": total,
            "completed": completed,
            "pending": pending,
            "completion_rate": completion_rate,
            "avg_streak": int(avg_streak)
        })
    
    # Convert to response model
    # Roman Urdu: Response model mein convert karna
    months_list = [
        MonthlyTrend(
            month=t["month"],
            total=t["total"],
            completed=t["completed"],
            pending=t["pending"],
            completion_rate=t["completion_rate"],
            avg_streak=t["avg_streak"]
        )
        for t in trends
    ]
    
    return MonthlyTrendsResponse(months=months_list)
