"""
Surveys Entity for ERP System.

This module provides entities for managing surveys and feedback
following Clean Architecture principles.
"""

from dataclasses import dataclass, field
from datetime import datetime, date
from typing import Optional, Dict, Any, List
from enum import Enum
from uuid import uuid4
from decimal import Decimal


class SurveyStatus(str, Enum):
    """Survey status enumeration."""
    DRAFT = "draft"
    ACTIVE = "active"
    CLOSED = "closed"
    ARCHIVED = "archived"


class QuestionType(str, Enum):
    """Survey question type enumeration."""
    TEXT = "text"
    MULTIPLE_CHOICE = "multiple_choice"
    SINGLE_CHOICE = "single_choice"
    RATING = "rating"
    SCALE = "scale"
    DATE = "date"
    EMAIL = "email"
    PHONE = "phone"


class ResponseStatus(str, Enum):
    """Response status enumeration."""
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    EXPIRED = "expired"


@dataclass(frozen=True)
class SurveyQuestion:
    """
    Value Object representing a survey question.
    Immutable and validated.
    """
    id: str
    question_text: str
    question_type: QuestionType
    is_required: bool = False
    options: List[str] = field(default_factory=list)
    min_value: Optional[int] = None
    max_value: Optional[int] = None
    placeholder: str = ""
    help_text: str = ""
    order: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "question_text": self.question_text,
            "question_type": self.question_type.value,
            "is_required": self.is_required,
            "options": self.options,
            "min_value": self.min_value,
            "max_value": self.max_value,
            "placeholder": self.placeholder,
            "help_text": self.help_text,
            "order": self.order
        }


@dataclass(frozen=True)
class SurveyResponse:
    """
    Value Object representing a survey response.
    Immutable and validated.
    """
    id: str
    respondent_id: Optional[str]
    respondent_email: str
    answers: Dict[str, Any]
    status: ResponseStatus
    submitted_at: Optional[datetime] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "respondent_id": self.respondent_id,
            "respondent_email": self.respondent_email,
            "answers": self.answers,
            "status": self.status.value,
            "submitted_at": self.submitted_at.isoformat() if self.submitted_at else None,
            "ip_address": self.ip_address,
            "user_agent": self.user_agent
        }


@dataclass(frozen=True)
class Survey:
    """
    Survey entity representing a survey/feedback form.
    
    This entity follows Clean Architecture principles and is immutable.
    
    Attributes:
        id: Unique identifier
        title: Survey title
        description: Survey description
        status: Current status
        questions: List of survey questions
        responses: List of responses
        starts_at: Start date
        ends_at: End date
        allow_anonymous: Allow anonymous responses
        allow_multiple: Allow multiple responses per user
        send_notifications: Send notifications on completion
        notify_emails: Email addresses to notify
        created_by: Creator user ID
        created_name: Creator name
        response_count: Number of responses
        completion_rate: Completion percentage
        average_rating: Average rating if applicable
        metadata: Additional metadata
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """
    id: str
    title: str
    description: str
    status: SurveyStatus
    questions: List[SurveyQuestion] = field(default_factory=list)
    responses: List[SurveyResponse] = field(default_factory=list)
    starts_at: Optional[date] = None
    ends_at: Optional[date] = None
    allow_anonymous: bool = True
    allow_multiple: bool = False
    send_notifications: bool = True
    notify_emails: List[str] = field(default_factory=list)
    created_by: str = ""
    created_name: str = ""
    response_count: int = 0
    completion_rate: Decimal = field(default=Decimal("0"))
    average_rating: Optional[Decimal] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    def __post_init__(self):
        if not self.title:
            raise ValueError("title cannot be empty")
    
    @property
    def is_active(self) -> bool:
        return self.status == SurveyStatus.ACTIVE
    
    @property
    def is_draft(self) -> bool:
        return self.status == SurveyStatus.DRAFT
    
    @property
    def is_open(self) -> bool:
        if not self.is_active:
            return False
        today = date.today()
        if self.starts_at and today < self.starts_at:
            return False
        if self.ends_at and today > self.ends_at:
            return False
        return True
    
    @property
    def question_count(self) -> int:
        return len(self.questions)
    
    @property
    def required_question_count(self) -> int:
        return sum(1 for q in self.questions if q.is_required)
    
    @property
    def completion_percentage(self) -> float:
        if self.response_count == 0:
            return 0.0
        completed = sum(1 for r in self.responses if r.status == ResponseStatus.COMPLETED)
        return (completed / self.response_count) * 100
    
    def calculate_statistics(self) -> Dict[str, Any]:
        """Calculate survey statistics."""
        total = len(self.responses)
        completed = sum(1 for r in self.responses if r.status == ResponseStatus.COMPLETED)
        
        ratings = []
        for response in self.responses:
            for question in self.questions:
                if question.question_type == QuestionType.RATING:
                    answer = response.answers.get(question.id)
                    if answer:
                        try:
                            ratings.append(int(answer))
                        except (ValueError, TypeError):
                            pass
        
        avg_rating = None
        if ratings:
            avg_rating = Decimal(str(sum(ratings) / len(ratings)))
        
        return {
            "total_responses": total,
            "completed_responses": completed,
            "in_progress_responses": total - completed,
            "completion_percentage": (completed / total * 100) if total > 0 else 0,
            "average_rating": str(avg_rating) if avg_rating else None,
            "rating_count": len(ratings)
        }
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status.value,
            "questions": [q.to_dict() for q in self.questions],
            "responses": [r.to_dict() for r in self.responses],
            "starts_at": self.starts_at.isoformat() if self.starts_at else None,
            "ends_at": self.ends_at.isoformat() if self.ends_at else None,
            "allow_anonymous": self.allow_anonymous,
            "allow_multiple": self.allow_multiple,
            "send_notifications": self.send_notifications,
            "notify_emails": self.notify_emails,
            "created_by": self.created_by,
            "created_name": self.created_name,
            "response_count": self.response_count,
            "completion_rate": str(self.completion_rate),
            "average_rating": str(self.average_rating) if self.average_rating else None,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "is_active": self.is_active,
            "is_draft": self.is_draft,
            "is_open": self.is_open,
            "question_count": self.question_count,
            "required_question_count": self.required_question_count,
            "statistics": self.calculate_statistics()
        }


class SurveyBuilder:
    """Builder for creating Survey instances."""
    
    def __init__(self):
        self._id: Optional[str] = None
        self._title: Optional[str] = None
        self._description: str = ""
        self._status: SurveyStatus = SurveyStatus.DRAFT
        self._questions: List[SurveyQuestion] = []
        self._responses: List[SurveyResponse] = []
        self._starts_at: Optional[date] = None
        self._ends_at: Optional[date] = None
        self._allow_anonymous: bool = True
        self._allow_multiple: bool = False
        self._send_notifications: bool = True
        self._notify_emails: List[str] = []
        self._created_by: str = ""
        self._created_name: str = ""
        self._metadata: Dict[str, Any] = {}
    
    def with_id(self, survey_id: str) -> "SurveyBuilder":
        self._id = survey_id
        return self
    
    def with_title(self, title: str) -> "SurveyBuilder":
        self._title = title
        return self
    
    def with_description(self, description: str) -> "SurveyBuilder":
        self._description = description
        return self
    
    def with_status(self, status: SurveyStatus) -> "SurveyBuilder":
        self._status = status
        return self
    
    def with_questions(self, questions: List[SurveyQuestion]) -> "SurveyBuilder":
        self._questions = questions
        return self
    
    def with_responses(self, responses: List[SurveyResponse]) -> "SurveyBuilder":
        self._responses = responses
        return self
    
    def with_dates(self, start: date, end: date) -> "SurveyBuilder":
        self._starts_at = start
        self._ends_at = end
        return self
    
    def with_anonymous(self, allow: bool) -> "SurveyBuilder":
        self._allow_anonymous = allow
        return self
    
    def with_multiple(self, allow: bool) -> "SurveyBuilder":
        self._allow_multiple = allow
        return self
    
    def with_notifications(self, send: bool, emails: List[str]) -> "SurveyBuilder":
        self._send_notifications = send
        self._notify_emails = emails
        return self
    
    def created_by(self, user_id: str, user_name: str) -> "SurveyBuilder":
        self._created_by = user_id
        self._created_name = user_name
        return self
    
    def with_metadata(self, metadata: Dict[str, Any]) -> "SurveyBuilder":
        self._metadata = metadata
        return self
    
    def build(self) -> Survey:
        if not self._id:
            self._id = str(uuid4())
        if not self._title:
            raise ValueError("title is required")
        
        return Survey(
            id=self._id,
            title=self._title,
            description=self._description,
            status=self._status,
            questions=self._questions,
            responses=self._responses,
            starts_at=self._starts_at,
            ends_at=self._ends_at,
            allow_anonymous=self._allow_anonymous,
            allow_multiple=self._allow_multiple,
            send_notifications=self._send_notifications,
            notify_emails=self._notify_emails,
            created_by=self._created_by,
            created_name=self._created_name,
            metadata=self._metadata
        )


def create_survey(
    title: str,
    **kwargs
) -> Survey:
    """Factory function to create a survey."""
    builder = SurveyBuilder()
    builder.with_title(title)
    
    if description := kwargs.get("description"):
        builder.with_description(description)
    if status := kwargs.get("status"):
        builder.with_status(status)
    if questions := kwargs.get("questions"):
        builder.with_questions(questions)
    if starts_at := kwargs.get("starts_at"):
        ends_at = kwargs.get("ends_at")
        builder.with_dates(starts_at, ends_at)
    if allow_anonymous := kwargs.get("allow_anonymous"):
        builder.with_anonymous(allow_anonymous)
    if allow_multiple := kwargs.get("allow_multiple"):
        builder.with_multiple(allow_multiple)
    if send_notifications := kwargs.get("send_notifications"):
        notify_emails = kwargs.get("notify_emails", [])
        builder.with_notifications(send_notifications, notify_emails)
    if created_by := kwargs.get("created_by"):
        created_name = kwargs.get("created_name", "")
        builder.created_by(created_by, created_name)
    if metadata := kwargs.get("metadata"):
        builder.with_metadata(metadata)
    
    return builder.build()


def create_question(
    question_text: str,
    question_type: QuestionType,
    **kwargs
) -> SurveyQuestion:
    """Factory function to create a survey question."""
    return SurveyQuestion(
        id=str(uuid4()),
        question_text=question_text,
        question_type=question_type,
        is_required=kwargs.get("is_required", False),
        options=kwargs.get("options", []),
        min_value=kwargs.get("min_value"),
        max_value=kwargs.get("max_value"),
        placeholder=kwargs.get("placeholder", ""),
        help_text=kwargs.get("help_text", ""),
        order=kwargs.get("order", 0)
    )
