"""
Report Entity - Domain Layer
Represents reports in the ERP system.

Author: Alexandre Albert Ndour
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional, Dict, Any
from enum import Enum
import uuid


class ReportType(str, Enum):
    """Report type enumeration."""
    SALES = "sales"
    INVENTORY = "inventory"
    FINANCIAL = "financial"
    CUSTOMER = "customer"
    EMPLOYEE = "employee"
    TAX = "tax"
    CUSTOM = "custom"


class ReportFormat(str, Enum):
    """Report format enumeration."""
    PDF = "pdf"
    EXCEL = "excel"
    CSV = "csv"
    HTML = "html"
    JSON = "json"


@dataclass
class Report:
    """
    Report Entity.
    
    Represents a generated report.
    """
    
    # Identity
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    name: str = ""
    report_type: ReportType = ReportType.SALES
    
    # Definition
    definition: Dict[str, Any] = field(default_factory=dict)
    
    # Parameters
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    filters: Dict[str, Any] = field(default_factory=dict)
    
    # Output
    format: ReportFormat = ReportFormat.PDF
    file_path: Optional[str] = None
    file_size: Optional[int] = None
    
    # Status
    status: str = "pending"  # pending, generating, completed, failed
    
    # Error
    error_message: Optional[str] = None
    
    # Scheduling
    is_scheduled: bool = False
    schedule_cron: Optional[str] = None
    
    # Access
    is_public: bool = False
    
    # Metadata
    generated_by: Optional[uuid.UUID] = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: Optional[datetime] = None
    
    # ==================== Business Methods ====================
    
    def start_generation(self, generated_by: uuid.UUID) -> None:
        """Start report generation."""
        self.status = "generating"
        self.generated_by = generated_by
    
    def complete(self, file_path: str, file_size: int) -> None:
        """Complete report generation."""
        self.status = "completed"
        self.file_path = file_path
        self.file_size = file_size
        self.completed_at = datetime.now(timezone.utc)
    
    def fail(self, error_message: str) -> None:
        """Mark report generation as failed."""
        self.status = "failed"
        self.error_message = error_message
        self.completed_at = datetime.now(timezone.utc)
    
    # ==================== Factory Methods ====================
    
    @classmethod
    def create(
        cls,
        name: str,
        report_type: ReportType,
        date_from: datetime = None,
        date_to: datetime = None,
        report_format: ReportFormat = ReportFormat.PDF,
        filters: Dict[str, Any] = None,
        generated_by: uuid.UUID = None
    ) -> "Report":
        """Factory method to create a report."""
        return cls(
            name=name,
            report_type=report_type,
            date_from=date_from,
            date_to=date_to,
            format=report_format,
            filters=filters or {},
            generated_by=generated_by
        )
    
    @classmethod
    def create_sales_report(
        cls,
        date_from: datetime,
        date_to: datetime,
        report_format: ReportFormat = ReportFormat.PDF,
        generated_by: uuid.UUID = None
    ) -> "Report":
        """Create a sales report."""
        return cls.create(
            name=f"Sales Report {date_from.date()} - {date_to.date()}",
            report_type=ReportType.SALES,
            date_from=date_from,
            date_to=date_to,
            report_format=report_format,
            generated_by=generated_by
        )
    
    @classmethod
    def create_inventory_report(
        cls,
        report_format: ReportFormat = ReportFormat.PDF,
        generated_by: uuid.UUID = None
    ) -> "Report":
        """Create an inventory report."""
        return cls.create(
            name=f"Inventory Report {datetime.now().date()}",
            report_type=ReportType.INVENTORY,
            report_format=report_format,
            generated_by=generated_by
        )
    
    # ==================== Serialization ====================
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "id": str(self.id),
            "name": self.name,
            "report_type": self.report_type.value,
            "date_from": self.date_from.isoformat() if self.date_from else None,
            "date_to": self.date_to.isoformat() if self.date_to else None,
            "format": self.format.value,
            "status": self.status,
            "file_path": self.file_path,
            "file_size": self.file_size,
            "error_message": self.error_message,
            "is_scheduled": self.is_scheduled,
            "generated_by": str(self.generated_by) if self.generated_by else None,
            "created_at": self.created_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }


@dataclass
class ReportSchedule:
    """
    ReportSchedule Entity.
    
    Represents a scheduled report.
    """
    
    # Identity
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    
    # Report definition
    name: str = ""
    report_type: ReportType = ReportType.SALES
    
    # Schedule
    cron_expression: str = ""
    frequency: str = "daily"  # daily, weekly, monthly
    
    # Parameters
    date_from_days_ago: int = 0
    date_to_days_ago: int = 0
    filters: Dict[str, Any] = field(default_factory=dict)
    
    # Output
    format: ReportFormat = ReportFormat.PDF
    recipients: list = field(default_factory=list)
    
    # Status
    is_active: bool = True
    last_run: Optional[datetime] = None
    next_run: Optional[datetime] = None
    
    # Metadata
    created_by: Optional[uuid.UUID] = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    
    def activate(self) -> None:
        """Activate schedule."""
        self.is_active = True
    
    def deactivate(self) -> None:
        """Deactivate schedule."""
        self.is_active = False
    
    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "name": self.name,
            "report_type": self.report_type.value,
            "cron_expression": self.cron_expression,
            "frequency": self.frequency,
            "format": self.format.value,
            "recipients": self.recipients,
            "is_active": self.is_active,
            "last_run": self.last_run.isoformat() if self.last_run else None,
            "next_run": self.next_run.isoformat() if self.next_run else None,
            "created_at": self.created_at.isoformat(),
        }
