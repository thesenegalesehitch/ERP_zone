"""
Task Entity for ERP System.

This module provides the Task entity for managing tasks/projects
following Clean Architecture principles.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from enum import Enum
from decimal import Decimal


class TaskStatus(str, Enum):
    """Task status enumeration."""
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    IN_REVIEW = "in_review"
    DONE = "done"
    CANCELLED = "cancelled"
    ON_HOLD = "on_hold"


class TaskPriority(str, Enum):
    """Task priority enumeration."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class TaskType(str, Enum):
    """Task type enumeration."""
    TASK = "task"
    BUG = "bug"
    FEATURE = "feature"
    IMPROVEMENT = "improvement"
    RESEARCH = "research"
    DOCUMENTATION = "documentation"


class RecurrencePattern(str, Enum):
    """Recurrence pattern for recurring tasks."""
    NONE = "none"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"


@dataclass(frozen=True)
class TaskTimeLog:
    """
    Value Object representing time logged to a task.
    Immutable and validated.
    """
    id: str
    user_id: str
    user_name: str
    hours: Decimal
    description: str
    logged_at: datetime = field(default_factory=datetime.utcnow)
    
    def __post_init__(self):
        if not self.user_id:
            raise ValueError("user_id cannot be empty")
        if self.hours <= 0:
            raise ValueError("hours must be positive")
        if not self.description:
            raise ValueError("description cannot be empty")
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "user_name": self.user_name,
            "hours": str(self.hours),
            "description": self.description,
            "logged_at": self.logged_at.isoformat()
        }


@dataclass(frozen=True)
class TaskComment:
    """
    Value Object representing a comment on a task.
    Immutable and validated.
    """
    id: str
    user_id: str
    user_name: str
    content: str
    created_at: datetime = field(default_factory=datetime.utcnow)
    
    def __post_init__(self):
        if not self.user_id:
            raise ValueError("user_id cannot be empty")
        if not self.content:
            raise ValueError("content cannot be empty")
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "user_name": self.user_name,
            "content": self.content,
            "created_at": self.created_at.isoformat()
        }


@dataclass(frozen=True)
class Task:
    """
    Task entity representing a task/project in the ERP system.
    
    This entity follows Clean Architecture principles and is immutable.
    
    Attributes:
        id: Unique identifier for the task
        task_number: Human-readable task number
        title: Task title
        description: Task description
        task_type: Type of task
        status: Current status
        priority: Priority level
        project_id: Associated project ID
        project_name: Associated project name
        assignee_id: ID of assignee
        assignee_name: Name of assignee
        reporter_id: ID of reporter
        reporter_name: Name of reporter
        due_date: estimated_hours: Estimated hours
        Due date
        actual_hours: Actual hours spent
        time_logs: List of time logs
        comments: List of comments
        attachments: List of attachment URLs
        tags: List of tags
        depends_on: List of dependent task IDs
        parent_id: Parent task ID (for subtasks)
        is_recurring: Whether task is recurring
        recurrence_pattern: Recurrence pattern
        metadata: Additional metadata
        created_at: Timestamp when created
        updated_at: Timestamp when last updated
        completed_at: Timestamp when completed
    """
    id: str
    task_number: str
    title: str
    description: str
    task_type: TaskType
    status: TaskStatus
    priority: TaskPriority
    project_id: Optional[str] = None
    project_name: Optional[str] = None
    assignee_id: Optional[str] = None
    assignee_name: Optional[str] = None
    reporter_id: Optional[str] = None
    reporter_name: Optional[str] = None
    due_date: Optional[datetime] = None
    estimated_hours: Optional[Decimal] = None
    actual_hours: Decimal = field(default=Decimal("0"))
    time_logs: List[TaskTimeLog] = field(default_factory=list)
    comments: List[TaskComment] = field(default_factory=list)
    attachments: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    depends_on: List[str] = field(default_factory=list)
    parent_id: Optional[str] = None
    is_recurring: bool = False
    recurrence_pattern: RecurrencePattern = RecurrencePattern.NONE
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Validate task after initialization."""
        if not self.task_number:
            raise ValueError("task_number cannot be empty")
        if not self.title:
            raise ValueError("title cannot be empty")
        if self.estimated_hours is not None and self.estimated_hours < 0:
            raise ValueError("estimated_hours cannot be negative")
        if self.actual_hours < 0:
            raise ValueError("actual_hours cannot be negative")
    
    @property
    def is_completed(self) -> bool:
        """Check if task is completed."""
        return self.status == TaskStatus.DONE
    
    @property
    def is_overdue(self) -> bool:
        """Check if task is overdue."""
        if not self.due_date:
            return False
        return datetime.utcnow() > self.due_date and not self.is_completed
    
    @property
    def is_assigned(self) -> bool:
        """Check if task is assigned."""
        return self.assignee_id is not None
    
    @property
    def progress_percent(self) -> Decimal:
        """Calculate progress percentage based on time."""
        if not self.estimated_hours or self.estimated_hours == 0:
            return Decimal("0")
        return min(Decimal("100"), (self.actual_hours / self.estimated_hours) * 100)
    
    @property
    def days_until_due(self) -> Optional[int]:
        """Get days until due date."""
        if not self.due_date:
            return None
        delta = self.due_date - datetime.utcnow()
        return delta.days
    
    @property
    def comment_count(self) -> int:
        """Get number of comments."""
        return len(self.comments)
    
    @property
    def time_log_count(self) -> int:
        """Get number of time logs."""
        return len(self.time_logs)
    
    def can_start(self) -> bool:
        """Check if task can be started."""
        if self.status not in [TaskStatus.TODO, TaskStatus.ON_HOLD]:
            return False
        for dep_id in self.depends_on:
            if dep_id not in [t.id for t in self.depends_on]:
                return False
        return True
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert task to dictionary."""
        return {
            "id": self.id,
            "task_number": self.task_number,
            "title": self.title,
            "description": self.description,
            "task_type": self.task_type.value,
            "status": self.status.value,
            "priority": self.priority.value,
            "project_id": self.project_id,
            "project_name": self.project_name,
            "assignee_id": self.assignee_id,
            "assignee_name": self.assignee_name,
            "reporter_id": self.reporter_id,
            "reporter_name": self.reporter_name,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "estimated_hours": str(self.estimated_hours) if self.estimated_hours else None,
            "actual_hours": str(self.actual_hours),
            "time_logs": [t.to_dict() for t in self.time_logs],
            "comments": [c.to_dict() for c in self.comments],
            "attachments": self.attachments,
            "tags": self.tags,
            "depends_on": self.depends_on,
            "parent_id": self.parent_id,
            "is_recurring": self.is_recurring,
            "recurrence_pattern": self.recurrence_pattern.value,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "is_completed": self.is_completed,
            "is_overdue": self.is_overdue,
            "is_assigned": self.is_assigned,
            "progress_percent": str(self.progress_percent),
            "days_until_due": self.days_until_due,
            "comment_count": self.comment_count,
            "time_log_count": self.time_log_count
        }


class TaskBuilder:
    """Builder for creating Task instances."""
    
    def __init__(self):
        self._id: Optional[str] = None
        self._task_number: Optional[str] = None
        self._title: Optional[str] = None
        self._description: str = ""
        self._task_type: TaskType = TaskType.TASK
        self._status: TaskStatus = TaskStatus.TODO
        self._priority: TaskPriority = TaskPriority.MEDIUM
        self._project_id: Optional[str] = None
        self._project_name: Optional[str] = None
        self._assignee_id: Optional[str] = None
        self._assignee_name: Optional[str] = None
        self._reporter_id: Optional[str] = None
        self._reporter_name: Optional[str] = None
        self._due_date: Optional[datetime] = None
        self._estimated_hours: Optional[Decimal] = None
        self._time_logs: List[TaskTimeLog] = []
        self._comments: List[TaskComment] = []
        self._attachments: List[str] = []
        self._tags: List[str] = []
        self._depends_on: List[str] = []
        self._parent_id: Optional[str] = None
        self._is_recurring: bool = False
        self._recurrence_pattern: RecurrencePattern = RecurrencePattern.NONE
        self._metadata: Dict[str, Any] = {}
    
    def with_id(self, task_id: str) -> "TaskBuilder":
        self._id = task_id
        return self
    
    def with_number(self, task_number: str) -> "TaskBuilder":
        self._task_number = task_number
        return self
    
    def with_title(self, title: str) -> "TaskBuilder":
        self._title = title
        return self
    
    def with_description(self, description: str) -> "TaskBuilder":
        self._description = description
        return self
    
    def with_type(self, task_type: TaskType) -> "TaskBuilder":
        self._task_type = task_type
        return self
    
    def with_status(self, status: TaskStatus) -> "TaskBuilder":
        self._status = status
        return self
    
    def with_priority(self, priority: TaskPriority) -> "TaskBuilder":
        self._priority = priority
        return self
    
    def for_project(self, project_id: str, project_name: str) -> "TaskBuilder":
        self._project_id = project_id
        self._project_name = project_name
        return self
    
    def assigned_to(self, assignee_id: str, assignee_name: str) -> "TaskBuilder":
        self._assignee_id = assignee_id
        self._assignee_name = assignee_name
        return self
    
    def reported_by(self, reporter_id: str, reporter_name: str) -> "TaskBuilder":
        self._reporter_id = reporter_id
        self._reporter_name = reporter_name
        return self
    
    def due_on(self, due_date: datetime) -> "TaskBuilder":
        self._due_date = due_date
        return self
    
    def with_estimate(self, hours: Decimal) -> "TaskBuilder":
        self._estimated_hours = hours
        return self
    
    def with_time_logs(self, time_logs: List[TaskTimeLog]) -> "TaskBuilder":
        self._time_logs = time_logs
        return self
    
    def add_time_log(self, time_log: TaskTimeLog) -> "TaskBuilder":
        self._time_logs.append(time_log)
        return self
    
    def with_comments(self, comments: List[TaskComment]) -> "TaskBuilder":
        self._comments = comments
        return self
    
    def add_comment(self, comment: TaskComment) -> "TaskBuilder":
        self._comments.append(comment)
        return self
    
    def with_attachments(self, attachments: List[str]) -> "TaskBuilder":
        self._attachments = attachments
        return self
    
    def with_tags(self, tags: List[str]) -> "TaskBuilder":
        self._tags = tags
        return self
    
    def depends_on_tasks(self, task_ids: List[str]) -> "TaskBuilder":
        self._depends_on = task_ids
        return self
    
    def as_subtask_of(self, parent_id: str) -> "TaskBuilder":
        self._parent_id = parent_id
        return self
    
    def recurring(self, pattern: RecurrencePattern) -> "TaskBuilder":
        self._is_recurring = True
        self._recurrence_pattern = pattern
        return self
    
    def with_metadata(self, metadata: Dict[str, Any]) -> "TaskBuilder":
        self._metadata = metadata
        return self
    
    def build(self) -> Task:
        from uuid import uuid4
        
        if not self._id:
            self._id = str(uuid4())
        if not self._task_number:
            from time import time
            self._task_number = f"TSK-{int(time())}"
        if not self._title:
            raise ValueError("title is required")
        
        return Task(
            id=self._id,
            task_number=self._task_number,
            title=self._title,
            description=self._description,
            task_type=self._task_type,
            status=self._status,
            priority=self._priority,
            project_id=self._project_id,
            project_name=self._project_name,
            assignee_id=self._assignee_id,
            assignee_name=self._assignee_name,
            reporter_id=self._reporter_id,
            reporter_name=self._reporter_name,
            due_date=self._due_date,
            estimated_hours=self._estimated_hours,
            time_logs=self._time_logs,
            comments=self._comments,
            attachments=self._attachments,
            tags=self._tags,
            depends_on=self._depends_on,
            parent_id=self._parent_id,
            is_recurring=self._is_recurring,
            recurrence_pattern=self._recurrence_pattern,
            metadata=self._metadata
        )


# Factory functions
def create_task_comment(
    user_id: str,
    user_name: str,
    content: str
) -> TaskComment:
    """Factory function to create a task comment."""
    from uuid import uuid4
    
    return TaskComment(
        id=str(uuid4()),
        user_id=user_id,
        user_name=user_name,
        content=content
    )


def create_task_time_log(
    user_id: str,
    user_name: str,
    hours: Decimal,
    description: str
) -> TaskTimeLog:
    """Factory function to create a time log."""
    from uuid import uuid4
    
    return TaskTimeLog(
        id=str(uuid4()),
        user_id=user_id,
        user_name=user_name,
        hours=hours,
        description=description
    )


def create_task(
    title: str,
    **kwargs
) -> Task:
    """Factory function to create a task."""
    builder = TaskBuilder()
    builder.with_title(title)
    
    if task_number := kwargs.get("task_number"):
        builder.with_number(task_number)
    if description := kwargs.get("description"):
        builder.with_description(description)
    if task_type := kwargs.get("task_type"):
        builder.with_type(task_type)
    if status := kwargs.get("status"):
        builder.with_status(status)
    if priority := kwargs.get("priority"):
        builder.with_priority(priority)
    if project_id := kwargs.get("project_id"):
        project_name = kwargs.get("project_name", "")
        builder.for_project(project_id, project_name)
    if assignee_id := kwargs.get("assignee_id"):
        assignee_name = kwargs.get("assignee_name", "")
        builder.assigned_to(assignee_id, assignee_name)
    if reporter_id := kwargs.get("reporter_id"):
        reporter_name = kwargs.get("reporter_name", "")
        builder.reported_by(reporter_id, reporter_name)
    if due_date := kwargs.get("due_date"):
        builder.due_on(due_date)
    if estimated_hours := kwargs.get("estimated_hours"):
        builder.with_estimate(estimated_hours)
    if tags := kwargs.get("tags"):
        builder.with_tags(tags)
    if parent_id := kwargs.get("parent_id"):
        builder.as_subtask_of(parent_id)
    if recurrence := kwargs.get("recurrence_pattern"):
        builder.recurring(recurrence)
    if metadata := kwargs.get("metadata"):
        builder.with_metadata(metadata)
    
    return builder.build()
