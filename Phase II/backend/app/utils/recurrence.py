"""
Recurrence Utility for Generating Recurring Tasks
Roman Urdu: Recurring tasks ke liye utility - daily, weekly, monthly tasks generate karne ke liye

Features:
- generate_recurring_instances(): Saare future occurrences ek saath generate karta hai
- Date calculations: daily (+1 day), weekly (+7 days), monthly (+1 month)

Roman Urdu Comments:
- Yeh utility recurring tasks ke saare instances ek saath calculate karta hai
- User ek baar request bhejta hai aur saare future tasks create ho jate hain
"""

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from typing import List, Dict


def generate_recurring_instances(
    start_date: datetime,
    recurrence_pattern: str,
    occurrences: int,
    title: str,
    description: str = None,
    priority: str = "medium",
    category_id: int = None
) -> List[Dict]:
    """
    Generate all occurrences for a recurring task
    
    Roman Urdu: Ek recurring task ke saare future instances ek saath generate karta hai.
    User ek baar request bhejta hai aur yeh function saare tasks calculate karta hai.
    
    Args:
        start_date: Pehle task ki date
        recurrence_pattern: daily, weekly, ya monthly
        occurrences: Kitne tasks generate karne hain (1-365)
        title: Task ka title
        description: Task ka description (optional)
        priority: Task ki priority (low, medium, high, urgent)
        category_id: Category ID (optional)
    
    Returns:
        List of dictionaries with task data for each occurrence
    
    Examples:
        # Daily standup for 30 days
        instances = generate_recurring_instances(
            start_date=datetime(2026, 3, 11),
            recurrence_pattern="daily",
            occurrences=30,
            title="Daily standup"
        )
        # Returns 30 tasks with incremented dates
        
        # Weekly meeting for 12 weeks
        instances = generate_recurring_instances(
            start_date=datetime(2026, 3, 11),
            recurrence_pattern="weekly",
            occurrences=12,
            title="Weekly team meeting"
        )
        
        # Monthly review for 6 months
        instances = generate_recurring_instances(
            start_date=datetime(2026, 3, 11),
            recurrence_pattern="monthly",
            occurrences=6,
            title="Monthly productivity review"
        )
    """
    instances = []
    
    for i in range(occurrences):
        # Calculate date for this occurrence
        # Roman Urdu: Har occurrence ke liye date calculate karna
        if recurrence_pattern == "daily":
            # Daily: +1 day for each occurrence
            # Roman Urdu: Roz ka task - ek din increment
            occurrence_date = start_date + timedelta(days=i)
        
        elif recurrence_pattern == "weekly":
            # Weekly: +7 days for each occurrence
            # Roman Urdu: Hafta ka task - 7 din increment
            occurrence_date = start_date + timedelta(weeks=i)
        
        elif recurrence_pattern == "monthly":
            # Monthly: +1 month for each occurrence
            # Roman Urdu: Mahine ka task - ek mahina increment
            # Using relativedelta for proper month handling
            # (e.g., Jan 31 + 1 month = Feb 28/29)
            occurrence_date = start_date + relativedelta(months=i)
        
        else:
            # Invalid pattern - should not happen due to schema validation
            # Roman Urdu: Invalid pattern - yeh schema validation mein catch ho jana chahiye
            raise ValueError(f"Invalid recurrence pattern: {recurrence_pattern}")
        
        # Create task instance data
        # Roman Urdu: Task instance ka data create karna
        instance_data = {
            "title": title,
            "description": description,
            "priority": priority,
            "due_date": occurrence_date,
            "recurrence_pattern": recurrence_pattern,
            "category_id": category_id,
            # parent_id will be set after the parent task is created
            "status": "pending",
            "is_deleted": False
        }
        
        instances.append(instance_data)
    
    return instances


def calculate_next_occurrence(
    current_date: datetime,
    recurrence_pattern: str
) -> datetime:
    """
    Calculate the next occurrence date from current date
    
    Roman Urdu: Current date se next occurrence ki date calculate karta hai
    
    Args:
        current_date: Current date
        recurrence_pattern: daily, weekly, ya monthly
    
    Returns:
        Next occurrence date
    
    Examples:
        next_date = calculate_next_occurrence(datetime(2026, 3, 11), "daily")
        # Returns: datetime(2026, 3, 12)
        
        next_date = calculate_next_occurrence(datetime(2026, 3, 11), "weekly")
        # Returns: datetime(2026, 3, 18)
        
        next_date = calculate_next_occurrence(datetime(2026, 1, 31), "monthly")
        # Returns: datetime(2026, 2, 28) - handles month end properly
    """
    if recurrence_pattern == "daily":
        return current_date + timedelta(days=1)
    
    elif recurrence_pattern == "weekly":
        return current_date + timedelta(weeks=1)
    
    elif recurrence_pattern == "monthly":
        return current_date + relativedelta(months=1)
    
    else:
        raise ValueError(f"Invalid recurrence pattern: {recurrence_pattern}")


def get_pattern_display_name(recurrence_pattern: str) -> str:
    """
    Get human-readable display name for recurrence pattern
    
    Roman Urdu: Recurrence pattern ka readable naam return karta hai
    
    Args:
        recurrence_pattern: daily, weekly, ya monthly
    
    Returns:
        Display name in Roman Urdu/English mix
    
    Examples:
        get_pattern_display_name("daily") -> "Rozana (Daily)"
        get_pattern_display_name("weekly") -> "Haftawar (Weekly)"
        get_pattern_display_name("monthly") -> "Mahinawar (Monthly)"
    """
    pattern_names = {
        "daily": "Rozana (Daily)",
        "weekly": "Haftawar (Weekly)",
        "monthly": "Mahinawar (Monthly)"
    }
    
    return pattern_names.get(recurrence_pattern, recurrence_pattern)
