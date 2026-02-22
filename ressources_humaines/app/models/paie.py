"""
Modèle de données pour la paie

Ce module définit le modèle de données pour la paie
dans le module des ressources humaines.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime, date
from typing import Optional


class PayrollModel:
    """Modèle de paie"""
    
    def __init__(
        self,
        id: int,
        employee_id: int,
        period_start: date,
        period_end: date,
        basic_salary: float = 0,
        overtime_hours: float = 0,
        overtime_rate: float = 1.5,
        bonuses: float = 0,
        allowances: float = 0,
        deductions: float = 0,
        gross_salary: float = 0,
        net_salary: float = 0,
        currency: str = "XOF",
        status: str = "brouillon",
        payment_date: Optional[date] = None,
        payment_method: Optional[str] = None,
        bank_transfer_reference: Optional[str] = None,
        notes: Optional[str] = None,
        processed_by: int = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.employee_id = employee_id
        self.period_start = period_start
        self.period_end = period_end
        self.basic_salary = basic_salary
        self.overtime_hours = overtime_hours
        self.overtime_rate = overtime_rate
        self.bonuses = bonuses
        self.allowances = allowances
        self.deductions = deductions
        self.gross_salary = gross_salary
        self.net_salary = net_salary
        self.currency = currency
        self.status = status
        self.payment_date = payment_date
        self.payment_method = payment_method
        self.bank_transfer_reference = bank_transfer_reference
        self.notes = notes
        self.processed_by = processed_by
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "employee_id": self.employee_id,
            "period_start": self.period_start,
            "period_end": self.period_end,
            "basic_salary": self.basic_salary,
            "overtime_hours": self.overtime_hours,
            "overtime_rate": self.overtime_rate,
            "bonuses": self.bonuses,
            "allowances": self.allowances,
            "deductions": self.deductions,
            "gross_salary": self.gross_salary,
            "net_salary": self.net_salary,
            "currency": self.currency,
            "status": self.status,
            "payment_date": self.payment_date,
            "payment_method": self.payment_method,
            "bank_transfer_reference": self.bank_transfer_reference,
            "notes": self.notes,
            "processed_by": self.processed_by,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "PayrollModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            employee_id=data.get("employee_id"),
            period_start=data.get("period_start"),
            period_end=data.get("period_end"),
            basic_salary=data.get("basic_salary", 0),
            overtime_hours=data.get("overtime_hours", 0),
            overtime_rate=data.get("overtime_rate", 1.5),
            bonuses=data.get("bonuses", 0),
            allowances=data.get("allowances", 0),
            deductions=data.get("deductions", 0),
            gross_salary=data.get("gross_salary", 0),
            net_salary=data.get("net_salary", 0),
            currency=data.get("currency", "XOF"),
            status=data.get("status", "brouillon"),
            payment_date=data.get("payment_date"),
            payment_method=data.get("payment_method"),
            bank_transfer_reference=data.get("bank_transfer_reference"),
            notes=data.get("notes"),
            processed_by=data.get("processed_by"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def calculate_gross(self) -> float:
        """Calcule le salaire brut"""
        overtime_pay = self.overtime_hours * self.basic_salary * self.overtime_rate / 160
        return self.basic_salary + overtime_pay + self.bonuses + self.allowances
    
    def calculate_net(self) -> float:
        """Calcule le salaire net"""
        return self.calculate_gross() - self.deductions
    
    def is_paid(self) -> bool:
        """Vérifie si payé"""
        return self.status == "paye"


class SalaryAdvanceModel:
    """Modèle d'avance sur salaire"""
    
    def __init__(
        self,
        id: int,
        employee_id: int,
        amount: float = 0,
        currency: str = "XOF",
        request_date: date = None,
        approval_date: Optional[date] = None,
        disbursement_date: Optional[date] = None,
        repayment_start_date: Optional[date] = None,
        installments: int = 1,
        installment_amount: float = 0,
        status: str = "en_attente",
        reason: Optional[str] = None,
        approved_by: Optional[int] = None,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.employee_id = employee_id
        self.amount = amount
        self.currency = currency
        self.request_date = request_date or date.today()
        self.approval_date = approval_date
        self.disbursement_date = disbursement_date
        self.repayment_start_date = repayment_start_date
        self.installments = installments
        self.installment_amount = installment_amount
        self.status = status
        self.reason = reason
        self.approved_by = approved_by
        self.notes = notes
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "employee_id": self.employee_id,
            "amount": self.amount,
            "currency": self.currency,
            "request_date": self.request_date,
            "approval_date": self.approval_date,
            "disbursement_date": self.disbursement_date,
            "repayment_start_date": self.repayment_start_date,
            "installments": self.installments,
            "installment_amount": self.installment_amount,
            "status": self.status,
            "reason": self.reason,
            "approved_by": self.approved_by,
            "notes": self.notes,
            "created_at": self.created_at
        }
    
    def is_approved(self) -> bool:
        """Vérifie si approuvé"""
        return self.status == "approuve"


class DeductionModel:
    """Modèle de retenue"""
    
    def __init__(
        self,
        id: int,
        payroll_id: int,
        deduction_type: str,
        description: str,
        amount: float = 0,
        is_taxable: bool = False,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.payroll_id = payroll_id
        self.deduction_type = deduction_type
        self.description = description
        self.amount = amount
        self.is_taxable = is_taxable
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "payroll_id": self.payroll_id,
            "deduction_type": self.deduction_type,
            "description": self.description,
            "amount": self.amount,
            "is_taxable": self.is_taxable,
            "created_at": self.created_at
        }
