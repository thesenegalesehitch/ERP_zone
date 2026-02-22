"""
Setting Entity for ERP System.

This module provides the Setting entity for managing application settings
following Clean Architecture principles.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any, List, Union
from enum import Enum


class SettingType(str, Enum):
    """Setting type enumeration."""
    STRING = "string"
    NUMBER = "number"
    BOOLEAN = "boolean"
    JSON = "json"
    SECRET = "secret"


class SettingCategory(str, Enum):
    """Setting category enumeration."""
    GENERAL = "general"
    COMPANY = "company"
    EMAIL = "email"
    NOTIFICATION = "notification"
    SECURITY = "security"
    PAYMENT = "payment"
    INTEGRATION = "integration"
    CUSTOM = "custom"


class SettingVisibility(str, Enum):
    """Setting visibility enumeration."""
    PUBLIC = "public"
    PRIVATE = "private"
    ADMIN = "admin"


@dataclass(frozen=True)
class Setting:
    """
    Setting entity representing a system/application setting.
    
    This entity follows Clean Architecture principles and is immutable.
    
    Attributes:
        id: Unique identifier for the setting
        key: Setting key/name
        value: Setting value
        setting_type: Type of setting value
        category: Setting category
        visibility: Who can view/edit the setting
        description: Setting description
        default_value: Default value
        is_encrypted: Whether value is encrypted
        is_system: Whether this is a system setting
        metadata: Additional metadata
        created_at: Timestamp when created
        updated_at: Timestamp when last updated
    """
    id: str
    key: str
    value: Any
    setting_type: SettingType
    category: SettingCategory
    visibility: SettingVisibility
    description: str
    default_value: Any = None
    is_encrypted: bool = False
    is_system: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    def __post_init__(self):
        """Validate setting after initialization."""
        if not self.key:
            raise ValueError("key cannot be empty")
        if not self.description:
            raise ValueError("description cannot be empty")
        if self.setting_type == SettingType.SECRET and not self.is_encrypted:
            raise ValueError("SECRET type must be encrypted")
    
    @property
    def is_secret(self) -> bool:
        """Check if setting is a secret."""
        return self.setting_type == SettingType.SECRET or self.is_encrypted
    
    @property
    def is_editable(self) -> bool:
        """Check if setting is editable."""
        return not self.is_system
    
    @property
    def masked_value(self) -> str:
        """Get masked value for secrets."""
        if self.is_secret:
            return "****"
        return str(self.value)
    
    def to_dict(self, include_secret: bool = False) -> Dict[str, Any]:
        """Convert setting to dictionary."""
        result = {
            "id": self.id,
            "key": self.key,
            "value": self.value if include_secret or not self.is_secret else self.masked_value,
            "setting_type": self.setting_type.value,
            "category": self.category.value,
            "visibility": self.visibility.value,
            "description": self.description,
            "default_value": self.default_value,
            "is_encrypted": self.is_encrypted,
            "is_system": self.is_system,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "is_secret": self.is_secret,
            "is_editable": self.is_editable
        }
        return result


class SettingBuilder:
    """Builder for creating Setting instances."""
    
    def __init__(self):
        self._id: Optional[str] = None
        self._key: Optional[str] = None
        self._value: Any = None
        self._setting_type: SettingType = SettingType.STRING
        self._category: SettingCategory = SettingCategory.GENERAL
        self._visibility: SettingVisibility = SettingVisibility.PRIVATE
        self._description: Optional[str] = None
        self._default_value: Any = None
        self._is_encrypted: bool = False
        self._is_system: bool = False
        self._metadata: Dict[str, Any] = {}
    
    def with_id(self, setting_id: str) -> "SettingBuilder":
        self._id = setting_id
        return self
    
    def with_key(self, key: str) -> "SettingBuilder":
        self._key = key
        return self
    
    def with_value(self, value: Any) -> "SettingBuilder":
        self._value = value
        return self
    
    def with_type(self, setting_type: SettingType) -> "SettingBuilder":
        self._setting_type = setting_type
        return self
    
    def in_category(self, category: SettingCategory) -> "SettingBuilder":
        self._category = category
        return self
    
    def with_visibility(self, visibility: SettingVisibility) -> "SettingBuilder":
        self._visibility = visibility
        return self
    
    def with_description(self, description: str) -> "SettingBuilder":
        self._description = description
        return self
    
    def with_default(self, default_value: Any) -> "SettingBuilder":
        self._default_value = default_value
        return self
    
    def encrypted(self, is_encrypted: bool = True) -> "SettingBuilder":
        self._is_encrypted = is_encrypted
        return self
    
    def as_system(self, is_system: bool = True) -> "SettingBuilder":
        self._is_system = is_system
        return self
    
    def with_metadata(self, metadata: Dict[str, Any]) -> "SettingBuilder":
        self._metadata = metadata
        return self
    
    def build(self) -> Setting:
        from uuid import uuid4
        
        if not self._id:
            self._id = str(uuid4())
        if not self._key:
            raise ValueError("key is required")
        if not self._description:
            raise ValueError("description is required")
        if self._value is None:
            self._value = self._default_value
        
        return Setting(
            id=self._id,
            key=self._key,
            value=self._value,
            setting_type=self._setting_type,
            category=self._category,
            visibility=self._visibility,
            description=self._description,
            default_value=self._default_value,
            is_encrypted=self._is_encrypted,
            is_system=self._is_system,
            metadata=self._metadata
        )


# Factory function
def create_setting(
    key: str,
    description: str,
    **kwargs
) -> Setting:
    """Factory function to create a setting."""
    builder = SettingBuilder()
    builder.with_key(key)
    builder.with_description(description)
    
    if value := kwargs.get("value"):
        builder.with_value(value)
    if setting_type := kwargs.get("setting_type"):
        builder.with_type(setting_type)
    if category := kwargs.get("category"):
        builder.in_category(category)
    if visibility := kwargs.get("visibility"):
        builder.with_visibility(visibility)
    if default_value := kwargs.get("default_value"):
        builder.with_default(default_value)
    if is_encrypted := kwargs.get("is_encrypted"):
        builder.encrypted(is_encrypted)
    if is_system := kwargs.get("is_system"):
        builder.as_system(is_system)
    if metadata := kwargs.get("metadata"):
        builder.with_metadata(metadata)
    
    return builder.build()
