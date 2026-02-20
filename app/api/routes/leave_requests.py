from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.leave_request import LeaveRequest
from app.models.user import User
from app.schemas.leave_request import LeaveRequestCreate, LeaveRequestResponse, LeaveRequestUpdate


router = APIRouter(prefix="/leave-requests", tags=["leave-requests"])


@router.get("/", response_model=list[LeaveRequestResponse], summary="Get all leave requests")
def get_leave_requests(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100,
):
    """
    Retrieve all leave requests with optional pagination
    """
    leave_requests = db.query(LeaveRequest).offset(skip).limit(limit).all()
    return leave_requests


@router.get("/{leave_request_id}", response_model=LeaveRequestResponse, summary="Get leave request by ID")
def get_leave_request(
    leave_request_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve a single leave request by ID
    """
    leave_request = db.query(LeaveRequest).filter(LeaveRequest.id == leave_request_id).first()
    if not leave_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Leave request not found"
        )
    return leave_request


@router.post("/", response_model=LeaveRequestResponse, status_code=status.HTTP_201_CREATED, summary="Create a new leave request")
def create_leave_request(
    leave_request_data: LeaveRequestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create a new leave request
    """
    db_leave_request = LeaveRequest(
        **leave_request_data.dict(),
        employee_id=current_user.employee.id if current_user.employee else None
    )
    db.add(db_leave_request)
    db.commit()
    db.refresh(db_leave_request)
    return db_leave_request


@router.put("/{leave_request_id}", response_model=LeaveRequestResponse, summary="Update leave request by ID")
def update_leave_request(
    leave_request_id: int,
    leave_request_data: LeaveRequestUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Update a leave request by ID
    """
    leave_request = db.query(LeaveRequest).filter(LeaveRequest.id == leave_request_id).first()
    if not leave_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Leave request not found"
        )

    for key, value in leave_request_data.dict(exclude_unset=True).items():
        setattr(leave_request, key, value)

    db.commit()
    db.refresh(leave_request)
    return leave_request


@router.delete("/{leave_request_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete leave request by ID")
def delete_leave_request(
    leave_request_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Delete a leave request by ID
    """
    leave_request = db.query(LeaveRequest).filter(LeaveRequest.id == leave_request_id).first()
    if not leave_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Leave request not found"
        )

    db.delete(leave_request)
    db.commit()
    return