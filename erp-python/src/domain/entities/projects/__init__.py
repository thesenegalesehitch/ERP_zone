"""
Project Entity for ERP System.

This module provides the Project entity for managing projects
following Clean Architecture principles.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from enum import Enum
from decimal import Decimal


class ProjectStatus(str, Enum):
    """Project status enumeration."""
    DRAFT = "draft"
    PLANNING = "planning"
    ACTIVE = "active"
    ON_HOLD = "on_hold"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    ARCHIVED = "archived"


class ProjectPriority(str, Enum):
    """Project priority enumeration."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ProjectPhase(str, Enum):
    """Project phase enumeration."""
    INITIATION = "initiation"
    PLANNING = "planning"
    EXECUTION = "execution"
    MONITORING = "monitoring"
    CLOSURE = "closure"


@dataclass(frozen=True)
class ProjectMilestone:
    """
    Value Object representing a project milestone.
    Immutable and validated.
    """
    id: str
    name: str
    description: str
    due_date: datetime
    completed_at: Optional[datetime] = None
    status: str = "pending"
    
    def __post_init__(self):
        if not self.name:
            raise ValueError("milestone name cannot be empty")
        if not self.description:
            raise ValueError("milestone description cannot be empty")
    
    @property
    def is_completed(self) -> bool:
        return self.completed_at is not None
    
    @property
    def is_overdue(self) -> bool:
        return not self.is_completed and datetime.utcnow() > self.due_date
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "due_date": self.due_date.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "status": self.status,
            "is_completed": self.is_completed,
            "is_overdue": self.is_overdue
        }


@dataclass(frozen=True)
class ProjectMember:
    """
    Value Object representing a project team member.
    Immutable and validated.
    """
    id: str
    user_id: str
    user_name: str
    user_email: str
    role: str
    joined_at: datetime = field(default_factory=datetime.utcnow)
    
    def __post_init__(self):
        if not self.user_id:
            raise ValueError("user_id cannot be empty")
        if not self.role:
            raise ValueError("role cannot be empty")
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "user_name": self.user_name,
            "user_email": self.user_email,
            "role": self.role,
            "joined_at": self.joined_at.isoformat()
        }


@dataclass(frozen=True)
class Project:
    """
    Project entity representing a project in the ERP system.
    
    This entity follows Clean Architecture principles and is immutable.
    
    Attributes:
        id: Unique identifier for the project
        project_code: Human-readable project code
        name: Project name
        description: Project description
        status: Current status
        priority: Priority level
        current_phase: Current project phase
        client_id: Client ID (if external)
        client_name: Client name
        start_date: Project start date
        end_date: Project end date
        budget: Project budget
        actual_cost: Actual cost incurred
        currency: Currency code
        manager_id: Project manager ID
        manager_name: Project manager name
        members: List of team members
        milestones: List of project milestones
        tags: List of tags
        goals: List of project goals
        risks: List of project risks
        metadata: Additional metadata
        created_at: Timestamp when created
        updated_at: Timestamp when last updated
        completed_at: Timestamp when completed
    """
    id: str
    project_code: str
    name: str
    description: str
    status: ProjectStatus
    priority: ProjectPriority
    current_phase: ProjectPhase
    client_id: Optional[str] = None
    client_name: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    budget: Optional[Decimal] = None
    actual_cost: Decimal = field(default=Decimal("0"))
    currency: str = "USD"
    manager_id: Optional[str] = None
    manager_name: Optional[str] = None
    members: List[ProjectMember] = field(default_factory=list)
    milestones: List[ProjectMilestone] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    goals: List[str] = field(default_factory=list)
    risks: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Validate project after initialization."""
        if not self.project_code:
            raise ValueError("project_code cannot be empty")
        if not self.name:
            raise ValueError("name cannot be empty")
        if self.budget is not None and self.budget < 0:
            raise ValueError("budget cannot be negative")
        if self.actual_cost < 0:
            raise ValueError("actual_cost cannot be negative")
        if self.start_date and self.end_date and self.end_date < self.start_date:
            raise ValueError("end_date must be after start_date")
    
    @property
    def is_active(self) -> bool:
        """Check if project is active."""
        return self.status == ProjectStatus.ACTIVE
    
    @property
    def is_completed(self) -> bool:
        """Check if project is completed."""
        return self.status == ProjectStatus.COMPLETED
    
    @property
    def is_overdue(self) -> bool:
        """Check if project is overdue."""
        if not self.end_date:
            return False
        return datetime.utcnow() > self.end_date and not self.is_completed
    
    @property
    def duration_days(self) -> Optional[int]:
        """Get project duration in days."""
        if not self.start_date or not self.end_date:
            return None
        delta = self.end_date - self.start_date
        return delta.days
    
    @property
    def days_remaining(self) -> Optional[int]:
        """Get days remaining until project end."""
        if not self.end_date:
            return None
        delta = self.end_date - datetime.utcnow()
        return max(0, delta.days)
    
    @property
    def budget_utilization(self) -> Decimal:
        """Calculate budget utilization percentage."""
        if not self.budget or self.budget == 0:
            return Decimal("0")
        return (self.actual_cost / self.budget) * 100
    
    @property
    def member_count(self) -> int:
        """Get number of team members."""
        return len(self.members)
    
    @property
    def milestone_count(self) -> int:
        """Get number of milestones."""
        return len(self.milestones)
    
    @property
    def completed_milestone_count(self) -> int:
        """Get number of completed milestones."""
        return sum(1 for m in self.milestones if m.is_completed)
    
    @property
    def progress_percent(self) -> Decimal:
        """Calculate project progress based on milestones."""
        if not self.milestones:
            return Decimal("0")
        completed = self.completed_milestone_count
        return (Decimal(completed) / Decimal(len(self.milestones))) * 100
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert project to dictionary."""
        return {
            "id": self.id,
            "project_code": self.project_code,
            "name": self.name,
            "description": self.description,
            "status": self.status.value,
            "priority": self.priority.value,
            "current_phase": self.current_phase.value,
            "client_id": self.client_id,
            "client_name": self.client_name,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "budget": str(self.budget) if self.budget else None,
            "actual_cost": str(self.actual_cost),
            "currency": self.currency,
            "manager_id": self.manager_id,
            "manager_name": self.manager_name,
            "members": [m.to_dict() for m in self.members],
            "milestones": [m.to_dict() for m in self.milestones],
            "tags": self.tags,
            "goals": self.goals,
            "risks": self.risks,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "is_active": self.is_active,
            "is_completed": self.is_completed,
            "is_overdue": self.is_overdue,
            "duration_days": self.duration_days,
            "days_remaining": self.days_remaining,
            "budget_utilization": str(self.budget_utilization),
            "member_count": self.member_count,
            "milestone_count": self.milestone_count,
            "completed_milestone_count": self.completed_milestone_count,
            "progress_percent": str(self.progress_percent)
        }


class ProjectBuilder:
    """Builder for creating Project instances."""
    
    def __init__(self):
        self._id: Optional[str] = None
        self._project_code: Optional[str] = None
        self._name: Optional[str] = None
        self._description: str = ""
        self._status: ProjectStatus = ProjectStatus.DRAFT
        self._priority: ProjectPriority = ProjectPriority.MEDIUM
        self._current_phase: ProjectPhase = ProjectPhase.INITIATION
        self._client_id: Optional[str] = None
        self._client_name: Optional[str] = None
        self._start_date: Optional[datetime] = None
        self._end_date: Optional[datetime] = None
        self._budget: Optional[Decimal] = None
        self._actual_cost: Decimal = Decimal("0")
        self._currency: str = "USD"
        self._manager_id: Optional[str] = None
        self._manager_name: Optional[str] = None
        self._members: List[ProjectMember] = []
        self._milestones: List[ProjectMilestone] = []
        self._tags: List[str] = []
        self._goals: List[str] = []
        self._risks: List[str] = []
        self._metadata: Dict[str, Any] = {}
    
    def with_id(self, project_id: str) -> "ProjectBuilder":
        self._id = project_id
        return self
    
    def with_code(self, project_code: str) -> "ProjectBuilder":
        self._project_code = project_code
        return self
    
    def with_name(self, name: str) -> "ProjectBuilder":
        self._name = name
        return self
    
    def with_description(self, description: str) -> "ProjectBuilder":
        self._description = description
        return self
    
    def with_status(self, status: ProjectStatus) -> "ProjectBuilder":
        self._status = status
        return self
    
    def with_priority(self, priority: ProjectPriority) -> "ProjectBuilder":
        self._priority = priority
        return self
    
    def in_phase(self, phase: ProjectPhase) -> "ProjectBuilder":
        self._current_phase = phase
        return self
    
    def for_client(self, client_id: str, client_name: str) -> "ProjectBuilder":
        self._client_id = client_id
        self._client_name = client_name
        return self
    
    def duration(self, start_date: datetime, end_date: datetime) -> "ProjectBuilder":
        self._start_date = start_date
        self._end_date = end_date
        return self
    
    def with_budget(self, budget: Decimal, currency: str = "USD") -> "ProjectBuilder":
        self._budget = budget
        self._currency = currency
        return self
    
    def managed_by(self, manager_id: str, manager_name: str) -> "ProjectBuilder":
        self._manager_id = manager_id
        self._manager_name = manager_name
        return self
    
    def with_members(self, members: List[ProjectMember]) -> "ProjectBuilder":
        self._members = members
        return self
    
    def add_member(self, member: ProjectMember) -> "ProjectBuilder":
        self._members.append(member)
        return self
    
    def with_milestones(self, milestones: List[ProjectMilestone]) -> "ProjectBuilder":
        self._milestones = milestones
        return self
    
    def add_milestone(self, milestone: ProjectMilestone) -> "ProjectBuilder":
        self._milestones.append(milestone)
        return self
    
    def with_tags(self, tags: List[str]) -> "ProjectBuilder":
        self._tags = tags
        return self
    
    def with_goals(self, goals: List[str]) -> "ProjectBuilder":
        self._goals = goals
        return self
    
    def with_risks(self, risks: List[str]) -> "ProjectBuilder":
        self._risks = risks
        return self
    
    def with_metadata(self, metadata: Dict[str, Any]) -> "ProjectBuilder":
        self._metadata = metadata
        return self
    
    def build(self) -> Project:
        from uuid import uuid4
        
        if not self._id:
            self._id = str(uuid4())
        if not self._project_code:
            from time import time
            self._project_code = f"PRJ-{int(time())}"
        if not self._name:
            raise ValueError("name is required")
        
        return Project(
            id=self._id,
            project_code=self._project_code,
            name=self._name,
            description=self._description,
            status=self._status,
            priority=self._priority,
            current_phase=self._current_phase,
            client_id=self._client_id,
            client_name=self._client_name,
            start_date=self._start_date,
            end_date=self._end_date,
            budget=self._budget,
            actual_cost=self._actual_cost,
            currency=self._currency,
            manager_id=self._manager_id,
            manager_name=self._manager_name,
            members=self._members,
            milestones=self._milestones,
            tags=self._tags,
            goals=self._goals,
            risks=self._risks,
            metadata=self._metadata
        )


# Factory functions
def create_project_member(
    user_id: str,
    user_name: str,
    user_email: str,
    role: str
) -> ProjectMember:
    """Factory function to create a project member."""
    from uuid import uuid4
    
    return ProjectMember(
        id=str(uuid4()),
        user_id=user_id,
        user_name=user_name,
        user_email=user_email,
        role=role
    )


def create_project_milestone(
    name: str,
    description: str,
    due_date: datetime
) -> ProjectMilestone:
    """Factory function to create a project milestone."""
    from uuid import uuid4
    
    return ProjectMilestone(
        id=str(uuid4()),
        name=name,
        description=description,
        due_date=due_date
    )


def create_project(
    name: str,
    **kwargs
) -> Project:
    """Factory function to create a project."""
    builder = ProjectBuilder()
    builder.with_name(name)
    
    if project_code := kwargs.get("project_code"):
        builder.with_code(project_code)
    if description := kwargs.get("description"):
        builder.with_description(description)
    if status := kwargs.get("status"):
        builder.with_status(status)
    if priority := kwargs.get("priority"):
        builder.with_priority(priority)
    if phase := kwargs.get("current_phase"):
        builder.in_phase(phase)
    if client_id := kwargs.get("client_id"):
        client_name = kwargs.get("client_name", "")
        builder.for_client(client_id, client_name)
    if start_date := kwargs.get("start_date"):
        end_date = kwargs.get("end_date")
        builder.duration(start_date, end_date)
    if budget := kwargs.get("budget"):
        currency = kwargs.get("currency", "USD")
        builder.with_budget(budget, currency)
    if manager_id := kwargs.get("manager_id"):
        manager_name = kwargs.get("manager_name", "")
        builder.managed_by(manager_id, manager_name)
    if members := kwargs.get("members"):
        builder.with_members(members)
    if milestones := kwargs.get("milestones"):
        builder.with_milestones(milestones)
    if tags := kwargs.get("tags"):
        builder.with_tags(tags)
    if goals := kwargs.get("goals"):
        builder.with_goals(goals)
    if risks := kwargs.get("risks"):
        builder.with_risks(risks)
    if metadata := kwargs.get("metadata"):
        builder.with_metadata(metadata)
    
    return builder.build()
