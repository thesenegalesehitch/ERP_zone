"""
API Layer - Invoice Controller
FastAPI routes for invoice management.

Author: Alexandre Albert Ndour
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Optional
import uuid

from ...application.dtos.invoices import (
    CreateInvoiceDTO,
    CreateInvoiceLineDTO,
    RecordPaymentDTO,
    InvoiceResponseDTO,
    InvoiceLineResponseDTO,
    InvoiceFilterDTO,
    PaginationParams,
)


router = APIRouter(prefix="/invoices", tags=["Invoices"])


@router.post(
    "/",
    response_model=InvoiceResponseDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new invoice",
    description="Create a new invoice"
)
async def create_invoice(
    dto: CreateInvoiceDTO,
    use_case=None,
    current_user=None
):
    """Create a new invoice."""
    try:
        result = await use_case.execute(dto, created_by=getattr(current_user, 'id', None))
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get(
    "/{invoice_id}",
    response_model=InvoiceResponseDTO,
    summary="Get invoice by ID",
    description="Retrieve an invoice by its unique identifier"
)
async def get_invoice(
    invoice_id: uuid.UUID,
    use_case=None,
    current_user=None
):
    """Get invoice by ID."""
    try:
        result = await use_case.execute(invoice_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get(
    "/",
    summary="List invoices",
    description="List invoices with pagination and filters"
)
async def list_invoices(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    customer_id: Optional[uuid.UUID] = None,
    status: Optional[str] = None,
    overdue_only: bool = Query(False),
    unpaid_only: bool = Query(False),
    use_case=None,
    current_user=None
):
    """List invoices with pagination."""
    try:
        filters = InvoiceFilterDTO(
            customer_id=customer_id,
            status=status,
            overdue_only=overdue_only,
            unpaid_only=unpaid_only
        )
        pagination = PaginationParams(page=page, limit=limit)
        
        invoices, total = await use_case.execute(filters, pagination)
        return invoices
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post(
    "/{invoice_id}/send",
    response_model=InvoiceResponseDTO,
    summary="Send invoice",
    description="Mark invoice as sent"
)
async def send_invoice(
    invoice_id: uuid.UUID,
    use_case=None,
    current_user=None
):
    """Send invoice."""
    try:
        result = await use_case.send(invoice_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post(
    "/{invoice_id}/payment",
    response_model=InvoiceResponseDTO,
    summary="Record payment",
    description="Record a payment for an invoice"
)
async def record_payment(
    invoice_id: uuid.UUID,
    dto: RecordPaymentDTO,
    use_case=None,
    current_user=None
):
    """Record payment."""
    try:
        result = await use_case.record_payment(invoice_id, dto)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post(
    "/{invoice_id}/mark-paid",
    response_model=InvoiceResponseDTO,
    summary="Mark as paid",
    description="Mark invoice as fully paid"
)
async def mark_as_paid(
    invoice_id: uuid.UUID,
    payment_method: Optional[str] = Query(None),
    reference: Optional[str] = Query(None),
    use_case=None,
    current_user=None
):
    """Mark invoice as paid."""
    try:
        result = await use_case.mark_paid(invoice_id, payment_method, reference)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post(
    "/{invoice_id}/cancel",
    response_model=InvoiceResponseDTO,
    summary="Cancel invoice",
    description="Cancel an invoice"
)
async def cancel_invoice(
    invoice_id: uuid.UUID,
    reason: str = Query(None),
    use_case=None,
    current_user=None
):
    """Cancel invoice."""
    try:
        result = await use_case.cancel(invoice_id, reason)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post(
    "/{invoice_id}/lines",
    response_model=InvoiceLineResponseDTO,
    summary="Add invoice line",
    description="Add a line item to an invoice"
)
async def add_invoice_line(
    invoice_id: uuid.UUID,
    dto: CreateInvoiceLineDTO,
    use_case=None,
    current_user=None
):
    """Add line to invoice."""
    try:
        result = await use_case.add_line(invoice_id, dto)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get(
    "/{invoice_id}/pdf",
    summary="Download invoice PDF",
    description="Download invoice as PDF"
)
async def download_pdf(
    invoice_id: uuid.UUID,
    use_case=None,
    current_user=None
):
    """Download invoice PDF."""
    try:
        result = await use_case.generate_pdf(invoice_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
