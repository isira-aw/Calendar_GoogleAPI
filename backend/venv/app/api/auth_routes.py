from fastapi import APIRouter, Query
from datetime import datetime
from typing import List, Dict

router = APIRouter()

# Dummy data storage for events
EVENTS_DB = [
    {"summary": "Team Meeting", "date": "2024-12-03"},
    {"summary": "Project Deadline", "date": "2024-12-15"},
    {"summary": "Doctor Appointment", "date": "2024-12-20"},
]

@router.get("/events")
def get_events(year: int = Query(...), month: int = Query(...)) -> Dict:
    """
    Fetch events for the given year and month.
    """
    # Format the month to always have two digits
    formatted_month = f"{month:02}"
    filtered_events = [
        event for event in EVENTS_DB if event["date"].startswith(f"{year}-{formatted_month}")
    ]
    return {"events": filtered_events}

@router.post("/events")
def add_event(summary: str, date: str) -> Dict:
    """
    Add a new event. Date format: YYYY-MM-DD.
    """
    try:
        # Validate date format
        datetime.strptime(date, "%Y-%m-%d")
        EVENTS_DB.append({"summary": summary, "date": date})
        return {"message": "Event added successfully!", "event": {"summary": summary, "date": date}}
    except ValueError:
        return {"error": "Invalid date format. Use YYYY-MM-DD."}
