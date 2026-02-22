"""
API Layer - Order Controller
FastAPI routes for order management.

Author: Alexandre Albert Ndour
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Optional, List
import uuid

from ...application.dtos.orders import (
    CreateOrderDTO,
    CreateOrderLineDTO,
    UpdateOrderStatusDTO,
    OrderResponseDTO,
    OrderLineResponseDTO,
    OrderFilterDTO,
    PaginationParams,
)


router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post(
    "/",
    response_model=OrderResponseDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new order",
    description="Create a new order"
)
async def create_order(
    dto: CreateOrderDTO,
    use_case=None,
    current_user=None
):
    """Create a new order."""
    try:
        result = await use_case.execute(dto, created_by=getattr(current_user, 'id', None))
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get(
    "/{order_id}",
    response_model=OrderResponseDTO,
    summary="Get order by ID",
    description="Retrieve an order by its unique identifier"
)
async def get_order(
    order_id: uuid.UUID,
    use_case=None,
    current_user=None
):
    """Get order by ID."""
    try:
        result = await use_case.execute(order_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get(
    "/",
    summary="List orders",
    description="List orders with pagination and filters"
)
async def list_orders(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    customer_id: Optional[uuid.UUID] = None,
    status: Optional[str] = None,
    payment_status: Optional[str] = None,
    search: Optional[str] = None,
    use_case=None,
    current_user=None
):
    """List orders with pagination."""
    try:
        filters = OrderFilterDTO(
            customer_id=customer_id,
            status=status,
            payment_status=payment_status,
            search=search
        )
        pagination = PaginationParams(page=page, limit=limit)
        
        orders, total = await use_case.execute(filters, pagination)
        return orders
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.put(
    "/{order_id}/status",
    response_model=OrderResponseDTO,
    summary="Update order status",
    description="Update the status of an order"
)
async def update_order_status(
    order_id: uuid.UUID,
    dto: UpdateOrderStatusDTO,
    use_case=None,
    current_user=None
):
    """Update order status."""
    try:
        result = await use_case.execute(order_id, dto)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post(
    "/{order_id}/lines",
    response_model=OrderLineResponseDTO,
    summary="Add order line",
    description="Add a line item to an order"
)
async def add_order_line(
    order_id: uuid.UUID,
    dto: CreateOrderLineDTO,
    use_case=None,
    current_user=None
):
    """Add a line to an order."""
    try:
        result = await use_case.execute(order_id, dto)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete(
    "/{order_id}/lines/{line_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove order line",
    description="Remove a line item from an order"
)
async def remove_order_line(
    order_id: uuid.UUID,
    line_id: uuid.UUID,
    use_case=None,
    current_user=None
):
    """Remove a line from an order."""
    try:
        await use_case.execute(order_id, line_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post(
    "/{order_id}/confirm",
    response_model=OrderResponseDTO,
    summary="Confirm order",
    description="Confirm an order"
)
async def confirm_order(
    order_id: uuid.UUID,
    use_case=None,
    current_user=None
):
    """Confirm an order."""
    try:
        result = await use_case.execute(order_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post(
    "/{order_id}/cancel",
    response_model=OrderResponseDTO,
    summary="Cancel order",
    description="Cancel an order"
)
async def cancel_order(
    order_id: uuid.UUID,
    reason: str = Query(None),
    use_case=None,
    current_user=None
):
    """Cancel an order."""
    try:
        result = await use_case.execute(order_id, reason)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get(
    "/{order_id}/lines",
    summary="Get order lines",
    description="Get all lines for an order"
)
async def get_order_lines(
    order_id: uuid.UUID,
    use_case=None,
    current_user=None
):
    """Get order lines."""
    try:
        result = await use_case.execute(order_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
