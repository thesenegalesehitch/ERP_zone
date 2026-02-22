"""
Product Entity - Domain Layer
Represents a product in the ERP system.

Author: Alexandre Albert Ndour
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional, List
import uuid


@dataclass
class Product:
    """
    Product Entity.
    
    Represents a product or service that can be sold.
    """
    
    # Identity
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    sku: str = ""
    name: str = ""
    description: str = ""
    
    # Pricing
    base_price: float = 0.0
    cost_price: float = 0.0
    tax_rate: float = 0.0
    
    # Classification
    category_id: Optional[uuid.UUID] = None
    brand: Optional[str] = None
    
    # Inventory
    track_inventory: bool = True
    current_stock: int = 0
    minimum_stock: int = 0
    maximum_stock: Optional[int] = None
    reorder_point: int = 0
    
    # Unit of measure
    unit: str = "unit"  # unit, kg, liter, meter, etc.
    
    # Status
    is_active: bool = True
    is_service: bool = False
    
    # Physical attributes
    weight: Optional[float] = None
    dimensions: Optional[str] = None  # LxWxH
    
    # Images
    image_urls: List[str] = field(default_factory=list)
    
    # Metadata
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    created_by: Optional[uuid.UUID] = None
    
    def __post_init__(self):
        """Validate after initialization."""
        if self.base_price < 0:
            raise ValueError("Base price cannot be negative")
        if self.cost_price < 0:
            raise ValueError("Cost price cannot be negative")
        if self.current_stock < 0:
            raise ValueError("Current stock cannot be negative")
    
    # ==================== Business Methods ====================
    
    def update_stock(self, quantity: int) -> None:
        """Update current stock quantity."""
        new_stock = self.current_stock + quantity
        if new_stock < 0:
            raise ValueError("Insufficient stock")
        self.current_stock = new_stock
        self.updated_at = datetime.now(timezone.utc)
    
    def set_price(self, price: float) -> None:
        """Set base price."""
        if price < 0:
            raise ValueError("Price cannot be negative")
        self.base_price = price
        self.updated_at = datetime.now(timezone.utc)
    
    def calculate_selling_price(self, markup_percent: float = 0) -> float:
        """Calculate selling price with optional markup."""
        if markup_percent > 0:
            return self.base_price * (1 + markup_percent / 100)
        return self.base_price
    
    def calculate_profit_margin(self) -> float:
        """Calculate profit margin percentage."""
        if self.base_price == 0:
            return 0
        return ((self.base_price - self.cost_price) / self.base_price) * 100
    
    def calculate_profit(self) -> float:
        """Calculate profit per unit."""
        return self.base_price - self.cost_price
    
    def is_low_stock(self) -> bool:
        """Check if stock is below reorder point."""
        return self.current_stock <= self.reorder_point
    
    def is_out_of_stock(self) -> bool:
        """Check if out of stock."""
        return self.current_stock <= 0
    
    def needs_reorder(self) -> bool:
        """Check if product needs reordering."""
        return self.track_inventory and self.current_stock <= self.reorder_point
    
    def activate(self) -> None:
        """Activate product."""
        self.is_active = True
        self.updated_at = datetime.now(timezone.utc)
    
    def deactivate(self) -> None:
        """Deactivate product."""
        self.is_active = False
        self.updated_at = datetime.now(timezone.utc)
    
    def add_image(self, url: str) -> None:
        """Add product image."""
        if url not in self.image_urls:
            self.image_urls.append(url)
            self.updated_at = datetime.now(timezone.utc)
    
    def remove_image(self, url: str) -> None:
        """Remove product image."""
        if url in self.image_urls:
            self.image_urls.remove(url)
            self.updated_at = datetime.now(timezone.utc)
    
    # ==================== Factory Methods ====================
    
    @classmethod
    def create(
        cls,
        sku: str,
        name: str,
        base_price: float,
        cost_price: float = 0,
        description: str = "",
        category_id: uuid.UUID = None,
        created_by: uuid.UUID = None
    ) -> "Product":
        """Factory method to create a new product."""
        return cls(
            sku=sku,
            name=name,
            base_price=base_price,
            cost_price=cost_price,
            description=description,
            category_id=category_id,
            created_by=created_by
        )
    
    @classmethod
    def create_service(
        cls,
        sku: str,
        name: str,
        price: float,
        description: str = ""
    ) -> "Product":
        """Factory method to create a service."""
        product = cls.create(
            sku=sku,
            name=name,
            base_price=price,
            description=description
        )
        product.is_service = True
        product.track_inventory = False
        return product
    
    # ==================== Serialization ====================
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "id": str(self.id),
            "sku": self.sku,
            "name": self.name,
            "description": self.description,
            "base_price": self.base_price,
            "cost_price": self.cost_price,
            "tax_rate": self.tax_rate,
            "category_id": str(self.category_id) if self.category_id else None,
            "brand": self.brand,
            "track_inventory": self.track_inventory,
            "current_stock": self.current_stock,
            "minimum_stock": self.minimum_stock,
            "maximum_stock": self.maximum_stock,
            "reorder_point": self.reorder_point,
            "unit": self.unit,
            "is_active": self.is_active,
            "is_service": self.is_service,
            "weight": self.weight,
            "dimensions": self.dimensions,
            "image_urls": self.image_urls,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
    
    def to_summary_dict(self) -> dict:
        """Convert to summary dictionary."""
        return {
            "id": str(self.id),
            "sku": self.sku,
            "name": self.name,
            "base_price": self.base_price,
            "current_stock": self.current_stock,
            "is_active": self.is_active,
            "is_low_stock": self.is_low_stock(),
        }
