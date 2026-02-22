"""
Shipping Entity for ERP System.

This module provides the Shipping entity for managing shipping
following Clean Architecture principles.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any, List
from enum import Enum
from decimal import Decimal


class ShippingStatus(str, Enum):
    """Shipping status enumeration."""
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    IN_TRANSIT = "in_transit"
    OUT_FOR_DELIVERY = "out_for_delivery"
    DELIVERED = "delivered"
    FAILED = "failed"
    RETURNED = "returned"
    CANCELLED = "cancelled"


class ShippingMethod(str, Enum):
    """Shipping method enumeration."""
    STANDARD = "standard"
    EXPRESS = "express"
    OVERNIGHT = "overnight"
    INTERNATIONAL = "international"
    PICKUP = "pickup"


class PackageStatus(str, Enum):
    """Package status enumeration."""
    CREATED = "created"
    PACKED = "packed"
    LABEL_PRINTED = "label_printed"
    PICKED_UP = "picked_up"
    IN_TRANSIT = "in_transit"
    DELIVERED = "delivered"
    EXCEPTION = "exception"


@dataclass(frozen=True)
class TrackingEvent:
    """
    Value Object representing a tracking event.
    Immutable and validated.
    """
    id: str
    status: str
    location: str
    description: str
    timestamp: datetime
    
    def __post_init__(self):
        if not self.status:
            raise ValueError("status cannot be empty")
        if not self.location:
            raise ValueError("location cannot be empty")
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "status": self.status,
            "location": self.location,
            "description": self.description,
            "timestamp": self.timestamp.isoformat()
        }


@dataclass(frozen=True)
class Shipping:
    """
    Shipping entity representing a shipment.
    
    This entity follows Clean Architecture principles and is immutable.
    
    Attributes:
        id: Unique identifier for the shipping
        tracking_number: Tracking number
        carrier: Shipping carrier name
        method: Shipping method
        status: Current status
        order_id: Associated order ID
        customer_id: Customer ID
        customer_name: Customer name
        sender_name: Sender name
        sender_address: Sender address
        recipient_name: Recipient name
        recipient_address: Recipient address
        recipient_phone: Recipient phone
        weight: Package weight (kg)
        dimensions: Package dimensions (L x W x H)
        shipping_cost: Shipping cost
        insurance_value: Insurance value
        signature_required: Whether signature is required
        tracking_events: List of tracking events
        estimated_delivery: Estimated delivery date
        actual_delivery: Actual delivery date
        metadata: Additional metadata
        created_at: Timestamp when created
        updated_at: Timestamp when last updated
    """
    id: str
    tracking_number: str
    carrier: str
    method: ShippingMethod
    status: ShippingStatus
    order_id: str
    customer_id: str
    customer_name: str
    sender_name: str
    sender_address: str
    recipient_name: str
    recipient_address: str
    recipient_phone: Optional[str] = None
    weight: Optional[Decimal] = None
    dimensions: Optional[str] = None
    shipping_cost: Optional[Decimal] = None
    insurance_value: Optional[Decimal] = None
    signature_required: bool = False
    tracking_events: List[TrackingEvent] = field(default_factory=list)
    estimated_delivery: Optional[datetime] = None
    actual_delivery: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    def __post_init__(self):
        """Validate shipping after initialization."""
        if not self.tracking_number:
            raise ValueError("tracking_number cannot be empty")
        if not self.carrier:
            raise ValueError("carrier cannot be empty")
        if not self.order_id:
            raise ValueError("order_id cannot be empty")
    
    @property
    def is_delivered(self) -> bool:
        """Check if shipment is delivered."""
        return self.status == ShippingStatus.DELIVERED
    
    @property
    def is_in_transit(self) -> bool:
        """Check if shipment is in transit."""
        return self.status in [ShippingStatus.IN_TRANSIT, ShippingStatus.OUT_FOR_DELIVERY]
    
    @property
    def is_cancelled(self) -> bool:
        """Check if shipment is cancelled."""
        return self.status == ShippingStatus.CANCELLED
    
    @property
    def tracking_event_count(self) -> int:
        """Get number of tracking events."""
        return len(self.tracking_events)
    
    @property
    def last_tracking_event(self) -> Optional[TrackingEvent]:
        """Get the most recent tracking event."""
        if not self.tracking_events:
            return None
        return sorted(self.tracking_events, key=lambda e: e.timestamp, reverse=True)[0]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert shipping to dictionary."""
        return {
            "id": self.id,
            "tracking_number": self.tracking_number,
            "carrier": self.carrier,
            "method": self.method.value,
            "status": self.status.value,
            "order_id": self.order_id,
            "customer_id": self.customer_id,
            "customer_name": self.customer_name,
            "sender_name": self.sender_name,
            "sender_address": self.sender_address,
            "recipient_name": self.recipient_name,
            "recipient_address": self.recipient_address,
            "recipient_phone": self.recipient_phone,
            "weight": str(self.weight) if self.weight else None,
            "dimensions": self.dimensions,
            "shipping_cost": str(self.shipping_cost) if self.shipping_cost else None,
            "insurance_value": str(self.insurance_value) if self.insurance_value else None,
            "signature_required": self.signature_required,
            "tracking_events": [e.to_dict() for e in self.tracking_events],
            "estimated_delivery": self.estimated_delivery.isoformat() if self.estimated_delivery else None,
            "actual_delivery": self.actual_delivery.isoformat() if self.actual_delivery else None,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "is_delivered": self.is_delivered,
            "is_in_transit": self.is_in_transit,
            "is_cancelled": self.is_cancelled,
            "tracking_event_count": self.tracking_event_count,
            "last_tracking_event": self.last_tracking_event.to_dict() if self.last_tracking_event else None
        }


class ShippingBuilder:
    """Builder for creating Shipping instances."""
    
    def __init__(self):
        self._id: Optional[str] = None
        self._tracking_number: Optional[str] = None
        self._carrier: Optional[str] = None
        self._method: ShippingMethod = ShippingMethod.STANDARD
        self._status: ShippingStatus = ShippingStatus.PENDING
        self._order_id: Optional[str] = None
        self._customer_id: Optional[str] = None
        self._customer_name: Optional[str] = None
        self._sender_name: Optional[str] = None
        self._sender_address: Optional[str] = None
        self._recipient_name: Optional[str] = None
        self._recipient_address: Optional[str] = None
        self._recipient_phone: Optional[str] = None
        self._weight: Optional[Decimal] = None
        self._dimensions: Optional[str] = None
        self._shipping_cost: Optional[Decimal] = None
        self._insurance_value: Optional[Decimal] = None
        self._signature_required: bool = False
        self._tracking_events: List[TrackingEvent] = []
        self._estimated_delivery: Optional[datetime] = None
        self._metadata: Dict[str, Any] = {}
    
    def with_id(self, shipping_id: str) -> "ShippingBuilder":
        self._id = shipping_id
        return self
    
    def with_tracking_number(self, tracking_number: str) -> "ShippingBuilder":
        self._tracking_number = tracking_number
        return self
    
    def with_carrier(self, carrier: str) -> "ShippingBuilder":
        self._carrier = carrier
        return self
    
    def with_method(self, method: ShippingMethod) -> "ShippingBuilder":
        self._method = method
        return self
    
    def with_status(self, status: ShippingStatus) -> "ShippingBuilder":
        self._status = status
        return self
    
    def for_order(self, order_id: str) -> "ShippingBuilder":
        self._order_id = order_id
        return self
    
    def to_customer(self, customer_id: str, customer_name: str) -> "ShippingBuilder":
        self._customer_id = customer_id
        self._customer_name = customer_name
        return self
    
    def from_sender(self, sender_name: str, sender_address: str) -> "ShippingBuilder":
        self._sender_name = sender_name
        self._sender_address = sender_address
        return self
    
    def to_recipient(self, recipient_name: str, recipient_address: str) -> "ShippingBuilder":
        self._recipient_name = recipient_name
        self._recipient_address = recipient_address
        return self
    
    def with_phone(self, phone: str) -> "ShippingBuilder":
        self._recipient_phone = phone
        return self
    
    def with_weight(self, weight: Decimal) -> "ShippingBuilder":
        self._weight = weight
        return self
    
    def with_dimensions(self, dimensions: str) -> "ShippingBuilder":
        self._dimensions = dimensions
        return self
    
    def with_cost(self, cost: Decimal) -> "ShippingBuilder":
        self._shipping_cost = cost
        return self
    
    def with_insurance(self, value: Decimal) -> "ShippingBuilder":
        self._insurance_value = value
        return self
    
    def requires_signature(self, required: bool = True) -> "ShippingBuilder":
        self._signature_required = required
        return self
    
    def with_tracking_events(self, events: List[TrackingEvent]) -> "ShippingBuilder":
        self._tracking_events = events
        return self
    
    def add_tracking_event(self, event: TrackingEvent) -> "ShippingBuilder":
        self._tracking_events.append(event)
        return self
    
    def estimated_delivery_on(self, date: datetime) -> "ShippingBuilder":
        self._estimated_delivery = date
        return self
    
    def with_metadata(self, metadata: Dict[str, Any]) -> "ShippingBuilder":
        self._metadata = metadata
        return self
    
    def build(self) -> Shipping:
        from uuid import uuid4
        
        if not self._id:
            self._id = str(uuid4())
        if not self._tracking_number:
            from time import time
            self._tracking_number = f"TRK-{int(time())}"
        if not self._carrier:
            raise ValueError("carrier is required")
        if not self._order_id:
            raise ValueError("order_id is required")
        
        return Shipping(
            id=self._id,
            tracking_number=self._tracking_number,
            carrier=self._carrier,
            method=self._method,
            status=self._status,
            order_id=self._order_id,
            customer_id=self._customer_id or "",
            customer_name=self._customer_name or "",
            sender_name=self._sender_name or "",
            sender_address=self._sender_address or "",
            recipient_name=self._recipient_name or "",
            recipient_address=self._recipient_address or "",
            recipient_phone=self._recipient_phone,
            weight=self._weight,
            dimensions=self._dimensions,
            shipping_cost=self._shipping_cost,
            insurance_value=self._insurance_value,
            signature_required=self._signature_required,
            tracking_events=self._tracking_events,
            estimated_delivery=self._estimated_delivery,
            metadata=self._metadata
        )


# Factory functions
def create_tracking_event(
    status: str,
    location: str,
    description: str,
    timestamp: datetime
) -> TrackingEvent:
    """Factory function to create a tracking event."""
    from uuid import uuid4
    
    return TrackingEvent(
        id=str(uuid4()),
        status=status,
        location=location,
        description=description,
        timestamp=timestamp
    )


def create_shipping(
    carrier: str,
    order_id: str,
    **kwargs
) -> Shipping:
    """Factory function to create a shipping."""
    builder = ShippingBuilder()
    builder.with_carrier(carrier)
    builder.for_order(order_id)
    
    if tracking_number := kwargs.get("tracking_number"):
        builder.with_tracking_number(tracking_number)
    if method := kwargs.get("method"):
        builder.with_method(method)
    if status := kwargs.get("status"):
        builder.with_status(status)
    if customer_id := kwargs.get("customer_id"):
        customer_name = kwargs.get("customer_name", "")
        builder.to_customer(customer_id, customer_name)
    if sender_name := kwargs.get("sender_name"):
        sender_address = kwargs.get("sender_address", "")
        builder.from_sender(sender_name, sender_address)
    if recipient_name := kwargs.get("recipient_name"):
        recipient_address = kwargs.get("recipient_address", "")
        builder.to_recipient(recipient_name, recipient_address)
    if phone := kwargs.get("recipient_phone"):
        builder.with_phone(phone)
    if weight := kwargs.get("weight"):
        builder.with_weight(weight)
    if dimensions := kwargs.get("dimensions"):
        builder.with_dimensions(dimensions)
    if cost := kwargs.get("shipping_cost"):
        builder.with_cost(cost)
    if insurance := kwargs.get("insurance_value"):
        builder.with_insurance(insurance)
    if signature_required := kwargs.get("signature_required"):
        builder.requires_signature(signature_required)
    if estimated_delivery := kwargs.get("estimated_delivery"):
        builder.estimated_delivery_on(estimated_delivery)
    if metadata := kwargs.get("metadata"):
        builder.with_metadata(metadata)
    
    return builder.build()
