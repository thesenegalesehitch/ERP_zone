"""
ProductCategory Entity - Domain Layer
Represents a product category in the ERP system.

Author: Alexandre Albert Ndour
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional, List
import uuid


@dataclass
class ProductCategory:
    """
    ProductCategory Entity.
    
    Represents a category for organizing products.
    Supports hierarchical categories (parent/child).
    """
    
    # Identity
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    name: str = ""
    slug: str = ""
    description: str = ""
    
    # Hierarchy
    parent_id: Optional[uuid.UUID] = None
    level: int = 0
    
    # Display
    display_order: int = 0
    image_url: Optional[str] = None
    
    # Status
    is_active: bool = True
    is_featured: bool = False
    
    # Metadata
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    
    def __post_init__(self):
        """Validate after initialization."""
        if self.slug == "" and self.name:
            self.slug = self.name.lower().replace(" ", "-")
    
    # ==================== Business Methods ====================
    
    def add_subcategory(self, category: "ProductCategory") -> None:
        """Add a subcategory."""
        category.parent_id = self.id
        category.level = self.level + 1
    
    def is_ancestor_of(self, category_id: uuid.UUID) -> bool:
        """Check if this category is an ancestor of another."""
        # Would need to check the category tree
        return False
    
    def is_descendant_of(self, category_id: uuid.UUID) -> bool:
        """Check if this category is a descendant of another."""
        return self.parent_id == category_id
    
    def get_ancestors(self) -> List[uuid.UUID]:
        """Get all ancestor category IDs."""
        ancestors = []
        if self.parent_id:
            ancestors.append(self.parent_id)
        return ancestors
    
    def activate(self) -> None:
        """Activate category."""
        self.is_active = True
        self.updated_at = datetime.now(timezone.utc)
    
    def deactivate(self) -> None:
        """Deactivate category."""
        self.is_active = False
        self.updated_at = datetime.now(timezone.utc)
    
    # ==================== Factory Methods ====================
    
    @classmethod
    def create(
        cls,
        name: str,
        description: str = "",
        parent_id: uuid.UUID = None
    ) -> "ProductCategory":
        """Factory method to create a new category."""
        return cls(
            name=name,
            description=description,
            parent_id=parent_id,
            level=0 if parent_id is None else 1
        )
    
    @classmethod
    def create_root(cls, name: str, description: str = "") -> "ProductCategory":
        """Factory method to create a root category."""
        return cls.create(name=name, description=description, parent_id=None)
    
    # ==================== Serialization ====================
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "id": str(self.id),
            "name": self.name,
            "slug": self.slug,
            "description": self.description,
            "parent_id": str(self.parent_id) if self.parent_id else None,
            "level": self.level,
            "display_order": self.display_order,
            "image_url": self.image_url,
            "is_active": self.is_active,
            "is_featured": self.is_featured,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


@dataclass
class ProductVariant:
    """
    ProductVariant Entity.
    
    Represents a variant of a product (e.g., size, color).
    """
    
    # Identity
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    product_id: uuid.UUID = None  # type: ignore
    
    # Variant attributes
    name: str = ""  # e.g., "Red / Large"
    sku_suffix: str = ""  # e.g., "-RED-LG"
    
    # Pricing override
    price_modifier: float = 0  # Additional price
    
    # Inventory
    stock: int = 0
    
    # Status
    is_active: bool = True
    
    # Metadata
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    
    # Attributes (JSON-like)
    attributes: dict = field(default_factory=dict)
    
    def __post_init__(self):
        if isinstance(self.product_id, str):
            self.product_id = uuid.UUID(self.product_id)
    
    def update_stock(self, quantity: int) -> None:
        """Update variant stock."""
        new_stock = self.stock + quantity
        if new_stock < 0:
            raise ValueError("Insufficient stock")
        self.stock = new_stock
        self.updated_at = datetime.now(timezone.utc)
    
    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "product_id": str(self.product_id),
            "name": self.name,
            "sku_suffix": self.sku_suffix,
            "price_modifier": self.price_modifier,
            "stock": self.stock,
            "is_active": self.is_active,
            "attributes": self.attributes,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
