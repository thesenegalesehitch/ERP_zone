"""
Calendar Event Entity for ERP System.

This module provides the CalendarEvent entity for managing calendar events
following Clean Architecture principles.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from enum import Enum


class CalendarEventStatus(str, Enum):
    """Calendar event status enumeration."""
    SCHEDULED = "scheduled"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"


class CalendarEventType(str, Enum):
    """Calendar event type enumeration."""
    MEETING = "meeting"
    CALL = "call"
    DEADLINE = "deadline"
    REMINDER = "reminder"
    TASK = "task"
    HOLIDAY = "holiday"
    OTHER = "other"


class RecurrenceFrequency(str, Enum):
    """Recurrence frequency enumeration."""
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"


@dataclass(frozen=True)
class CalendarEvent:
    """
    CalendarEvent entity representing a calendar event.
    
    This entity follows Clean Architecture principles and is immutable.
    
    Attributes:
        id: Unique identifier for the event
        title: Event title
        description: Event description
        event_type: Type of event
        status: Current status
        start_time: Event start time
        end_time: Event end time
        all_day: Whether event is all day
        timezone: Event timezone
        location: Event location
        organizer_id: ID of organizer
        organizer_name: Name of organizer
        attendees: List of attendee emails
        is_recurring: Whether event is recurring
        recurrence_rule: Recurrence rule
        recurrence_end: End of recurrence
        parent_id: Parent event ID (for recurring events)
        reminders: List of reminder times (in minutes)
        metadata: Additional metadata
        created_at: Timestamp when created
        updated_at: Timestamp when last updated
    """
    id: str
    title: str
    description: str
    event_type: CalendarEventType
    status: CalendarEventStatus
    start_time: datetime
    end_time: datetime
    all_day: bool = False
    timezone: str = "UTC"
    location: Optional[str] = None
    organizer_id: Optional[str] = None
    organizer_name: Optional[str] = None
    attendees: List[str] = field(default_factory=list)
    is_recurring: bool = False
    recurrence_rule: Optional[str] = None
    recurrence_end: Optional[datetime] = None
    parent_id: Optional[str] = None
    reminders: List[int] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    def __post_init__(self):
        """Validate calendar event after initialization."""
        if not self.title:
            raise ValueError("title cannot be empty")
        if self.end_time < self.start_time:
            raise ValueError("end_time must be after start_time")
    
    @property
    def is_upcoming(self) -> bool:
        """Check if event is upcoming."""
        return self.start_time > datetime.utcnow() and self.status != CalendarEventStatus.CANCELLED
    
    @property
    def is_past(self) -> bool:
        """Check if event is in the past."""
        return self.end_time < datetime.utcnow()
    
    @property
    def duration_minutes(self) -> int:
        """Get event duration in minutes."""
        delta = self.end_time - self.start_time
        return int(delta.total_seconds() / 60)
    
    @property
    def attendee_count(self) -> int:
        """Get number of attendees."""
        return len(self.attendees)
    
    @property
    def reminder_count(self) -> int:
        """Get number of reminders."""
        return len(self.reminders)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "event_type": self.event_type.value,
            "status": self.status.value,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "all_day": self.all_day,
            "timezone": self.timezone,
            "location": self.location,
            "organizer_id": self.organizer_id,
            "organizer_name": self.organizer_name,
            "attendees": self.attendees,
            "is_recurring": self.is_recurring,
            "recurrence_rule": self.recurrence_rule,
            "recurrence_end": self.recurrence_end.isoformat() if self.recurrence_end else None,
            "parent_id": self.parent_id,
            "reminders": self.reminders,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "is_upcoming": self.is_upcoming,
            "is_past": self.is_past,
            "duration_minutes": self.duration_minutes,
            "attendee_count": self.attendee_count,
            "reminder_count": self.reminder_count
        }


class CalendarEventBuilder:
    """Builder for creating CalendarEvent instances."""
    
    def __init__(self):
        self._id: Optional[str] = None
        self._title: Optional[str] = None
        self._description: str = ""
        self._event_type: CalendarEventType = CalendarEventType.MEETING
        self._status: CalendarEventStatus = CalendarEventStatus.SCHEDULED
        self._start_time: Optional[datetime] = None
        self._end_time: Optional[datetime] = None
        self._all_day: bool = False
        self._timezone: str = "UTC"
        self._location: Optional[str] = None
        self._organizer_id: Optional[str] = None
        self._organizer_name: Optional[str] = None
        self._attendees: List[str] = []
        self._is_recurring: bool = False
        self._recurrence_rule: Optional[str] = None
        self._recurrence_end: Optional[datetime] = None
        self._parent_id: Optional[str] = None
        self._reminders: List[int] = []
        self._metadata: Dict[str, Any] = {}
    
    def with_id(self, event_id: str) -> "CalendarEventBuilder":
        self._id = event_id
        return self
    
    def with_title(self, title: str) -> "CalendarEventBuilder":
        self._title = title
        return self
    
    def with_description(self, description: str) -> "CalendarEventBuilder":
        self._description = description
        return self
    
    def with_type(self, event_type: CalendarEventType) -> "CalendarEventBuilder":
        self._event_type = event_type
        return self
    
    def with_status(self, status: CalendarEventStatus) -> "CalendarEventBuilder":
        self._status = status
        return self
    
    def scheduled(self, start_time: datetime, end_time: datetime) -> "CalendarEventBuilder":
        self._start_time = start_time
        self._end_time = end_time
        return self
    
    def all_day_event(self, date: datetime) -> "CalendarEventBuilder":
        self._all_day = True
        self._start_time = date.replace(hour=0, minute=0, second=0)
        self._end_time = date.replace(hour=23, minute=59, second=59)
        return self
    
    def in_timezone(self, timezone: str) -> "CalendarEventBuilder":
        self._timezone = timezone
        return self
    
    def at_location(self, location: str) -> "CalendarEventBuilder":
        self._location = location
        return self
    
    def organized_by(self, organizer_id: str, organizer_name: str) -> "CalendarEventBuilder":
        self._organizer_id = organizer_id
        self._organizer_name = organizer_name
        return self
    
    def with_attendees(self, attendees: List[str]) -> "CalendarEventBuilder":
        self._attendees = attendees
        return self
    
    def recurring(self, recurrence_rule: str, recurrence_end: Optional[datetime] = None) -> "CalendarEventBuilder":
        self._is_recurring = True
        self._recurrence_rule = recurrence_rule
        self._recurrence_end = recurrence_end
        return self
    
    def as_subevent_of(self, parent_id: str) -> "CalendarEventBuilder":
        self._parent_id = parent_id
        return self
    
    def with_reminders(self, reminders: List[int]) -> "CalendarEventBuilder":
        self._reminders = reminders
        return self
    
    def with_metadata(self, metadata: Dict[str, Any]) -> "CalendarEventBuilder":
        self._metadata = metadata
        return self
    
    def build(self) -> CalendarEvent:
        from uuid import uuid4
        
        if not self._id:
            self._id = str(uuid4())
        if not self._title:
            raise ValueError("title is required")
        if not self._start_time:
            raise ValueError("start_time is required")
        if not self._end_time:
            raise ValueError("end_time is required")
        
        return CalendarEvent(
            id=self._id,
            title=self._title,
            description=self._description,
            event_type=self._event_type,
            status=self._status,
            start_time=self._start_time,
            end_time=self._end_time,
            all_day=self._all_day,
            timezone=self._timezone,
            location=self._location,
            organizer_id=self._organizer_id,
            organizer_name=self._organizer_name,
            attendees=self._attendees,
            is_recurring=self._is_recurring,
            recurrence_rule=self._recurrence_rule,
            recurrence_end=self._recurrence_end,
            parent_id=self._parent_id,
            reminders=self._reminders,
            metadata=self._metadata
        )


# Factory function
def create_calendar_event(
    title: str,
    start_time: datetime,
    end_time: datetime,
    **kwargs
) -> CalendarEvent:
    """Factory function to create a calendar event."""
    builder = CalendarEventBuilder()
    builder.with_title(title)
    builder.scheduled(start_time, end_time)
    
    if description := kwargs.get("description"):
        builder.with_description(description)
    if event_type := kwargs.get("event_type"):
        builder.with_type(event_type)
    if status := kwargs.get("status"):
        builder.with_status(status)
    if all_day := kwargs.get("all_day"):
        builder.all_day_event(all_day)
    if timezone := kwargs.get("timezone"):
        builder.in_timezone(timezone)
    if location := kwargs.get("location"):
        builder.at_location(location)
    if organizer_id := kwargs.get("organizer_id"):
        organizer_name = kwargs.get("organizer_name", "")
        builder.organized_by(organizer_id, organizer_name)
    if attendees := kwargs.get("attendees"):
        builder.with_attendees(attendees)
    if recurrence_rule := kwargs.get("recurrence_rule"):
        recurrence_end = kwargs.get("recurrence_end")
        builder.recurring(recurrence_rule, recurrence_end)
    if parent_id := kwargs.get("parent_id"):
        builder.as_subevent_of(parent_id)
    if reminders := kwargs.get("reminders"):
        builder.with_reminders(reminders)
    if metadata := kwargs.get("metadata"):
        builder.with_metadata(metadata)
    
    return builder.build()
