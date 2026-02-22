"""
Settings Entity - Domain Layer
Represents application settings.

Author: Alexandre Albert Ndour
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional, Any, Dict
import uuid


@dataclass
class Setting:
    """
    Setting Entity.
    
    Represents a system configuration setting.
    """
    
    # Identity
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    key: str = ""
    
    # Value
    value: Any = None
    value_type: str = "string"  # string, number, boolean, json
    
    # Metadata
    category: str = "general"  # general, company, invoice, email, tax, payment
    description: Optional[str] = None
    
    # Access
    is_public: bool = False
    is_system: bool = False  # System settings cannot be modified
    
    # Validation
    validation_rule: Optional[str] = None
    
    # Metadata
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_by: Optional[uuid.UUID] = None
    
    # ==================== Business Methods ====================
    
    def update(self, value: Any, updated_by: uuid.UUID = None) -> None:
        """Update setting value."""
        if self.is_system:
            raise ValueError("Cannot modify system setting")
        
        self.value = value
        self.updated_at = datetime.now(timezone.utc)
        self.updated_by = updated_by
    
    def get_typed_value(self) -> Any:
        """Get value with proper type."""
        if self.value_type == "boolean":
            return str(self.value).lower() in ("true", "1", "yes")
        elif self.value_type == "number":
            return float(self.value)
        elif self.value_type == "json":
            import json
            return json.loads(self.value)
        return self.value
    
    # ==================== Factory Methods ====================
    
    @classmethod
    def create(
        cls,
        key: str,
        value: Any,
        value_type: str = "string",
        category: str = "general",
        description: str = None,
        is_public: bool = False,
        is_system: bool = False
    ) -> "Setting":
        """Factory method to create a setting."""
        if isinstance(value, dict):
            value_type = "json"
            import json
            value = json.dumps(value)
        
        return cls(
            key=key,
            value=value,
            value_type=value_type,
            category=category,
            description=description,
            is_public=is_public,
            is_system=is_system
        )
    
    @classmethod
    def create_company_setting(
        cls,
        key: str,
        value: Any,
        value_type: str = "string"
    ) -> "Setting":
        """Create a company setting."""
        return cls.create(
            key=f"company.{key}",
            value=value,
            value_type=value_type,
            category="company"
        )
    
    @classmethod
    def create_invoice_setting(
        cls,
        key: str,
        value: Any,
        value_type: str = "string"
    ) -> "Setting":
        """Create an invoice setting."""
        return cls.create(
            key=f"invoice.{key}",
            value=value,
            value_type=value_type,
            category="invoice"
        )
    
    # ==================== Serialization ====================
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "id": str(self.id),
            "key": self.key,
            "value": self.value,
            "value_type": self.value_type,
            "category": self.category,
            "description": self.description,
            "is_public": self.is_public,
            "is_system": self.is_system,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


@dataclass
class SettingGroup:
    """
    SettingGroup Entity.
    
    Represents a group of related settings.
    """
    
    # Identity
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    name: str = ""
    slug: str = ""
    description: Optional[str] = None
    
    # Display
    icon: Optional[str] = None
    display_order: int = 0
    
    # Status
    is_active: bool = True
    
    # Settings count
    _settings: list = field(default_factory=list, repr=False)
    
    def add_setting(self, setting: Setting) -> None:
        """Add a setting to the group."""
        self._settings.append(setting)
    
    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "name": self.name,
            "slug": self.slug,
            "description": self.description,
            "icon": self.icon,
            "display_order": self.display_order,
            "is_active": self.is_active,
            "settings_count": len(self._settings),
        }


# Default system settings
DEFAULT_SETTINGS = [
    # Company settings
    {"key": "company.name", "value": "", "category": "company", "is_system": True},
    {"key": "company.address", "value": "", "category": "company", "is_system": True},
    {"key": "company.phone", "value": "", "category": "company", "is_system": True},
    {"key": "company.email", "value": "", "category": "company", "is_system": True},
    {"key": "company.website", "value": "", "category": "company", "is_system": True},
    {"key": "company.tax_id", "value": "", "category": "company", "is_system": True},
    
    # Invoice settings
    {"key": "invoice.prefix", "value": "INV", "category": "invoice", "is_system": True},
    {"key": "invoice.next_number", "value": 1, "value_type": "number", "category": "invoice", "is_system": True},
    {"key": "invoice.default_due_days", "value": 30, "value_type": "number", "category": "invoice", "is_system": True},
    {"key": "invoice.default_tax_rate", "value": 20, "value_type": "number", "category": "invoice", "is_system": True},
    
    # Order settings
    {"key": "order.prefix", "value": "ORD", "category": "order", "is_system": True},
    {"key": "order.auto_confirm", "value": "false", "value_type": "boolean", "category": "order", "is_system": True},
    
    # Currency
    {"key": "currency.default", "value": "EUR", "category": "general", "is_system": True},
    {"key": "currency.supported", "value": ["EUR", "USD", "GBP"], "value_type": "json", "category": "general", "is_system": True},
    
    # Locale
    {"key": "locale.timezone", "value": "UTC", "category": "general", "is_system": True},
    {"key": "locale.language", "value": "en", "category": "general", "is_system": True},
    {"key": "locale.date_format", "value": "YYYY-MM-DD", "category": "general", "is_system": True},
]
