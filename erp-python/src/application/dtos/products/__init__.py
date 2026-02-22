"""
Application Layer - Product DTOs
Data Transfer Objects for Product operations.

Author: Alexandre Albert Ndour
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List
import uuid


@dataclass
class CreateProductDTO:
    """DTO for creating a new product."""
    sku: str
    name: str
    description: str = ""
    base_price: float = 0.0
    cost_price: float = 0.0
    tax_rate: float = 0.0
    category_id: Optional[uuid.UUID] = None
    brand: Optional[str] = None
    track_inventory: bool = True
    minimum_stock: int = 0
    reorder_point: int = 0
    unit: str = "unit"
    is_service: bool = False
    weight: Optional[float] = None
    dimensions: Optional[str] = None


@dataclass
class UpdateProductDTO:
    """DTO for updating a product."""
    name: Optional[str] = None
    description: Optional[str] = None
    base_price: Optional[float] = None
    cost_price: Optional[float] = None
    tax_rate: Optional[float] = None
    category_id: Optional[uuid.UUID] = None
    brand: Optional[str] = None
    track_inventory: Optional[bool] = None
    minimum_stock: Optional[int] = None
    reorder_point: Optional[int] = None
    unit: Optional[str] = None
    is_active: Optional[bool] = None
    weight: Optional[float] = None
    dimensions: Optional[str] = None


@dataclass
class ProductResponseDTO:
    """DTO for product response."""
    id: uuid.UUID
    sku: str
    name: str
    description: str
    base_price: float
    cost_price: float
    tax_rate: float
    category_id: Optional[uuid.UUID]
    brand: Optional[str]
    track_inventory: bool
    current_stock: int
    minimum_stock: int
    reorder_point: int
    unit: str
    is_active: bool
    is_service: bool
    weight: Optional[float]
    dimensions: Optional[str]
    image_urls: List[str]
    created_at: datetime
    updated_at: datetime


@dataclass
class ProductListDTO:
    """DTO for product list response."""
    id: uuid.UUID
    sku: str
    name: str
    base_price: float
    current_stock: int
    is_active: bool
    is_low_stock: bool


@dataclass
class CreateCategoryDTO:
    """DTO for creating a category."""
    name: str
    description: str = ""
    parent_id: Optional[uuid.UUID] = None
    image_url: Optional[str] = None
    is_featured: bool = False


@dataclass
class CategoryResponseDTO:
    """DTO for category response."""
    id: uuid.UUID
    name: str
    slug: str
    description: str
    parent_id: Optional[uuid.UUID]
    level: int
    image_url: Optional[str]
    is_active: bool
    is_featured: bool
    created_at: datetime


@dataclass
class StockAdjustmentDTO:
    """DTO for stock adjustment."""
    product_id: uuid.UUID
    quantity: int
    reason: str
    notes: Optional[str] = None


@dataclass
class StockMovementResponseDTO:
    """DTO for stock movement response."""
    id: uuid.UUID
    product_id: uuid.UUID
    movement_type: str
    reason: str
    quantity: int
    quantity_before: int
    quantity_after: int
    notes: Optional[str]
    performed_by: Optional[uuid.UUID]
    created_at: datetime


@dataclass
class ProductFilterDTO:
    """Filter parameters for product list."""
    category_id: Optional[uuid.UUID] = None
    is_active: Optional[bool] = None
    is_service: Optional[bool] = None
    search: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    in_stock_only: bool = False
    low_stock_only: bool = False


@dataclass
class PaginationParams:
    """Pagination parameters."""
    page: int = 1
    limit: int = 20
    sort_by: str = "created_at"
    sort_order: str = "desc"
    
    @property
    def offset(self) -> int:
        return (self.page - 1) * self.limit
