"""
Analytics Entity for ERP System.

This module provides the Analytics entity for tracking analytics data
following Clean Architecture principles.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any, List
from enum import Enum
from decimal import Decimal


class AnalyticsEventType(str, Enum):
    """Analytics event type enumeration."""
    PAGE_VIEW = "page_view"
    CLICK = "click"
    CONVERSION = "conversion"
    PURCHASE = "purchase"
    SIGNUP = "signup"
    LOGIN = "login"
    LOGOUT = "logout"
    ERROR = "error"
    CUSTOM = "custom"


class MetricType(str, Enum):
    """Metric type enumeration."""
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    SUMMARY = "summary"


@dataclass(frozen=True)
class AnalyticsEvent:
    """
    AnalyticsEvent entity representing a single analytics event.
    
    This entity follows Clean Architecture principles and is immutable.
    
    Attributes:
        id: Unique identifier for the event
        event_type: Type of analytics event
        event_name: Custom event name
        user_id: ID of user who triggered event
        session_id: Session ID
        entity_type: Associated entity type
        entity_id: Associated entity ID
        properties: Event properties
        referrer: Referrer URL
        user_agent: User agent string
        ip_address: Client IP address
        metadata: Additional metadata
        timestamp: When event occurred
    """
    id: str
    event_type: AnalyticsEventType
    event_name: str
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    entity_type: Optional[str] = None
    entity_id: Optional[str] = None
    properties: Dict[str, Any] = field(default_factory=dict)
    referrer: Optional[str] = None
    user_agent: Optional[str] = None
    ip_address: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.utcnow)
    
    def __post_init__(self):
        """Validate analytics event after initialization."""
        if not self.event_name:
            raise ValueError("event_name cannot be empty")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary."""
        return {
            "id": self.id,
            "event_type": self.event_type.value,
            "event_name": self.event_name,
            "user_id": self.user_id,
            "session_id": self.session_id,
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
            "properties": self.properties,
            "referrer": self.referrer,
            "user_agent": self.user_agent,
            "ip_address": self.ip_address,
            "metadata": self.metadata,
            "timestamp": self.timestamp.isoformat()
        }


@dataclass(frozen=True)
class AnalyticsMetric:
    """
    AnalyticsMetric entity representing a metric data point.
    
    This entity follows Clean Architecture principles and is immutable.
    
    Attributes:
        id: Unique identifier for the metric
        name: Metric name
        metric_type: Type of metric
        value: Metric value
        unit: Unit of measurement
        entity_type: Associated entity type
        entity_id: Associated entity ID
        tags: Metric tags
        metadata: Additional metadata
        recorded_at: When metric was recorded
    """
    id: str
    name: str
    metric_type: MetricType
    value: Decimal
    unit: str = ""
    entity_type: Optional[str] = None
    entity_id: Optional[str] = None
    tags: Dict[str, str] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    recorded_at: datetime = field(default_factory=datetime.utcnow)
    
    def __post_init__(self):
        """Validate analytics metric after initialization."""
        if not self.name:
            raise ValueError("name cannot be empty")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert metric to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "metric_type": self.metric_type.value,
            "value": str(self.value),
            "unit": self.unit,
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
            "tags": self.tags,
            "metadata": self.metadata,
            "recorded_at": self.recorded_at.isoformat()
        }


class AnalyticsEventBuilder:
    """Builder for creating AnalyticsEvent instances."""
    
    def __init__(self):
        self._id: Optional[str] = None
        self._event_type: AnalyticsEventType = AnalyticsEventType.CUSTOM
        self._event_name: Optional[str] = None
        self._user_id: Optional[str] = None
        self._session_id: Optional[str] = None
        self._entity_type: Optional[str] = None
        self._entity_id: Optional[str] = None
        self._properties: Dict[str, Any] = {}
        self._referrer: Optional[str] = None
        self._user_agent: Optional[str] = None
        self._ip_address: Optional[str] = None
        self._metadata: Dict[str, Any] = {}
    
    def with_id(self, event_id: str) -> "AnalyticsEventBuilder":
        self._id = event_id
        return self
    
    def with_type(self, event_type: AnalyticsEventType) -> "AnalyticsEventBuilder":
        self._event_type = event_type
        return self
    
    def with_name(self, event_name: str) -> "AnalyticsEventBuilder":
        self._event_name = event_name
        return self
    
    def by_user(self, user_id: str) -> "AnalyticsEventBuilder":
        self._user_id = user_id
        return self
    
    def in_session(self, session_id: str) -> "AnalyticsEventBuilder":
        self._session_id = session_id
        return self
    
    def for_entity(self, entity_type: str, entity_id: str) -> "AnalyticsEventBuilder":
        self._entity_type = entity_type
        self._entity_id = entity_id
        return self
    
    def with_properties(self, properties: Dict[str, Any]) -> "AnalyticsEventBuilder":
        self._properties = properties
        return self
    
    def from_referrer(self, referrer: str) -> "AnalyticsEventBuilder":
        self._referrer = referrer
        return self
    
    def with_user_agent(self, user_agent: str) -> "AnalyticsEventBuilder":
        self._user_agent = user_agent
        return self
    
    def from_ip(self, ip_address: str) -> "AnalyticsEventBuilder":
        self._ip_address = ip_address
        return self
    
    def with_metadata(self, metadata: Dict[str, Any]) -> "AnalyticsEventBuilder":
        self._metadata = metadata
        return self
    
    def build(self) -> AnalyticsEvent:
        from uuid import uuid4
        
        if not self._id:
            self._id = str(uuid4())
        if not self._event_name:
            raise ValueError("event_name is required")
        
        return AnalyticsEvent(
            id=self._id,
            event_type=self._event_type,
            event_name=self._event_name,
            user_id=self._user_id,
            session_id=self._session_id,
            entity_type=self._entity_type,
            entity_id=self._entity_id,
            properties=self._properties,
            referrer=self._referrer,
            user_agent=self._user_agent,
            ip_address=self._ip_address,
            metadata=self._metadata
        )


class AnalyticsMetricBuilder:
    """Builder for creating AnalyticsMetric instances."""
    
    def __init__(self):
        self._id: Optional[str] = None
        self._name: Optional[str] = None
        self._metric_type: MetricType = MetricType.COUNTER
        self._value: Optional[Decimal] = None
        self._unit: str = ""
        self._entity_type: Optional[str] = None
        self._entity_id: Optional[str] = None
        self._tags: Dict[str, str] = {}
        self._metadata: Dict[str, Any] = {}
    
    def with_id(self, metric_id: str) -> "AnalyticsMetricBuilder":
        self._id = metric_id
        return self
    
    def with_name(self, name: str) -> "AnalyticsMetricBuilder":
        self._name = name
        return self
    
    def with_type(self, metric_type: MetricType) -> "AnalyticsMetricBuilder":
        self._metric_type = metric_type
        return self
    
    def with_value(self, value: Decimal, unit: str = "") -> "AnalyticsMetricBuilder":
        self._value = value
        self._unit = unit
        return self
    
    def for_entity(self, entity_type: str, entity_id: str) -> "AnalyticsMetricBuilder":
        self._entity_type = entity_type
        self._entity_id = entity_id
        return self
    
    def with_tags(self, tags: Dict[str, str]) -> "AnalyticsMetricBuilder":
        self._tags = tags
        return self
    
    def with_metadata(self, metadata: Dict[str, Any]) -> "AnalyticsMetricBuilder":
        self._metadata = metadata
        return self
    
    def build(self) -> AnalyticsMetric:
        from uuid import uuid4
        
        if not self._id:
            self._id = str(uuid4())
        if not self._name:
            raise ValueError("name is required")
        if self._value is None:
            raise ValueError("value is required")
        
        return AnalyticsMetric(
            id=self._id,
            name=self._name,
            metric_type=self._metric_type,
            value=self._value,
            unit=self._unit,
            entity_type=self._entity_type,
            entity_id=self._entity_id,
            tags=self._tags,
            metadata=self._metadata
        )


# Factory functions
def create_analytics_event(
    event_name: str,
    event_type: AnalyticsEventType = AnalyticsEventType.CUSTOM,
    **kwargs
) -> AnalyticsEvent:
    """Factory function to create an analytics event."""
    builder = AnalyticsEventBuilder()
    builder.with_name(event_name)
    builder.with_type(event_type)
    
    if user_id := kwargs.get("user_id"):
        builder.by_user(user_id)
    if session_id := kwargs.get("session_id"):
        builder.in_session(session_id)
    if entity_type := kwargs.get("entity_type"):
        entity_id = kwargs.get("entity_id", "")
        builder.for_entity(entity_type, entity_id)
    if properties := kwargs.get("properties"):
        builder.with_properties(properties)
    if referrer := kwargs.get("referrer"):
        builder.from_referrer(referrer)
    if user_agent := kwargs.get("user_agent"):
        builder.with_user_agent(user_agent)
    if ip_address := kwargs.get("ip_address"):
        builder.from_ip(ip_address)
    if metadata := kwargs.get("metadata"):
        builder.with_metadata(metadata)
    
    return builder.build()


def create_analytics_metric(
    name: str,
    value: Decimal,
    metric_type: MetricType = MetricType.COUNTER,
    **kwargs
) -> AnalyticsMetric:
    """Factory function to create an analytics metric."""
    builder = AnalyticsMetricBuilder()
    builder.with_name(name)
    builder.with_value(value, kwargs.get("unit", ""))
    builder.with_type(metric_type)
    
    if entity_type := kwargs.get("entity_type"):
        entity_id = kwargs.get("entity_id", "")
        builder.for_entity(entity_type, entity_id)
    if tags := kwargs.get("tags"):
        builder.with_tags(tags)
    if metadata := kwargs.get("metadata"):
        builder.with_metadata(metadata)
    
    return builder.build()
