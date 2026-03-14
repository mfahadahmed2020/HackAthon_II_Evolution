"""
Analytics Service Package Initialization
Roman Urdu: Analytics Service package
"""

from app.services.analytics_service import (
    get_or_create_analytics,
    update_analytics_on_task_create,
    update_analytics_on_task_complete,
    update_analytics_on_task_delete,
    calculate_streak,
    get_longest_streak,
    get_category_breakdown,
    get_weekly_trends,
)

__all__ = [
    "get_or_create_analytics",
    "update_analytics_on_task_create",
    "update_analytics_on_task_complete",
    "update_analytics_on_task_delete",
    "calculate_streak",
    "get_longest_streak",
    "get_category_breakdown",
    "get_weekly_trends",
]
