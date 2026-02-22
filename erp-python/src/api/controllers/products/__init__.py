"""
API Layer - Product Controller
FastAPI routes for product management.

Author: Alexandre Albert Ndour
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Optional, List
import uuid

from ...application.dtos.products import (
    CreateProductDTO,
    UpdateProductDTO,
    ProductResponseDTO,
    ProductListDTO,
    CreateCategoryDTO,
    CategoryResponseDTO,
    StockAdjustmentDTO,
    ProductFilterDTO,
    PaginationParams,
)


router = APIRouter(prefix="/products", tags=["Products"])


@router.post(
    "/",
    response_model=ProductResponseDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new product",
    description="Create a new product in the catalog"
)
async def create_product(
    dto: CreateProductDTO,
    use_case=None,
    current_user=None
):
    """Create a new product."""
    try:
        result = await use_case.execute(dto, created_by=getattr(current_user, 'id', None))
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get(
    "/{product_id}",
    response_model=ProductResponseDTO,
    summary="Get product by ID",
    description="Retrieve a product by its unique identifier"
)
async def get_product(
    product_id: uuid.UUID,
    use_case=None,
    current_user=None
):
    """Get product by ID."""
    try:
        result = await use_case.execute(product_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get(
    "/",
    response_model=List[ProductListDTO],
    summary="List products",
    description="List products with pagination and filters"
)
async def list_products(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    category_id: Optional[uuid.UUID] = None,
    is_active: Optional[bool] = None,
    search: Optional[str] = None,
    in_stock_only: bool = Query(False),
    low_stock_only: bool = Query(False),
    use_case=None,
    current_user=None
):
    """List products with pagination."""
    try:
        filters = ProductFilterDTO(
            category_id=category_id,
            is_active=is_active,
            search=search,
            in_stock_only=in_stock_only,
            low_stock_only=low_stock_only
        )
        pagination = PaginationParams(page=page, limit=limit)
        
        products, total = await use_case.execute(filters, pagination)
        return products
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.put(
    "/{product_id}",
    response_model=ProductResponseDTO,
    summary="Update product",
    description="Update product information"
)
async def update_product(
    product_id: uuid.UUID,
    dto: UpdateProductDTO,
    use_case=None,
    current_user=None
):
    """Update product."""
    try:
        result = await use_case.execute(product_id, dto)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete product",
    description="Delete a product"
)
async def delete_product(
    product_id: uuid.UUID,
    use_case=None,
    current_user=None
):
    """Delete product."""
    try:
        await use_case.execute(product_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post(
    "/{product_id}/stock",
    summary="Adjust stock",
    description="Adjust product stock quantity"
)
async def adjust_stock(
    product_id: uuid.UUID,
    dto: StockAdjustmentDTO,
    use_case=None,
    current_user=None
):
    """Adjust product stock."""
    try:
        result = await use_case.execute(
            product_id,
            dto,
            performed_by=getattr(current_user, 'id', None)
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get(
    "/{product_id}/stock/history",
    summary="Get stock history",
    description="Get product stock movement history"
)
async def get_stock_history(
    product_id: uuid.UUID,
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=100),
    use_case=None,
    current_user=None
):
    """Get stock movement history."""
    try:
        result = await use_case.execute(product_id, page, limit)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


# Category routes
category_router = APIRouter(prefix="/categories", tags=["Categories"])


@category_router.post(
    "/",
    response_model=CategoryResponseDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Create a category",
    description="Create a new product category"
)
async def create_category(
    dto: CreateCategoryDTO,
    use_case=None,
    current_user=None
):
    """Create a category."""
    try:
        result = await use_case.execute(dto)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@category_router.get(
    "/",
    summary="List categories",
    description="List all product categories"
)
async def list_categories(
    parent_id: Optional[uuid.UUID] = None,
    use_case=None,
    current_user=None
):
    """List categories."""
    try:
        result = await use_case.execute(parent_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


router.include_router(category_router)
