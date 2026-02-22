"""
Modèle de données pour les rapports financiers

Ce module définit le modèle de données pour les rapports
dans le module de comptabilité.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime, date
from typing import Optional


class FinancialReportModel:
    """Modèle de rapport financier"""
    
    def __init__(
        self,
        id: int,
        report_type: str,
        title: str,
        period_start: date,
        period_end: date,
        currency: str = "XOF",
        total_revenue: float = 0,
        total_expenses: float = 0,
        net_income: float = 0,
        status: str = "brouillon",
        generated_by: int = None,
        generated_at: Optional[datetime] = None,
        approved_by: Optional[int] = None,
        approved_at: Optional[datetime] = None,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.report_type = report_type
        self.title = title
        self.period_start = period_start
        self.period_end = period_end
        self.currency = currency
        self.total_revenue = total_revenue
        self.total_expenses = total_expenses
        self.net_income = net_income
        self.status = status
        self.generated_by = generated_by
        self.generated_at = generated_at
        self.approved_by = approved_by
        self.approved_at = approved_at
        self.notes = notes
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "report_type": self.report_type,
            "title": self.title,
            "period_start": self.period_start,
            "period_end": self.period_end,
            "currency": self.currency,
            "total_revenue": self.total_revenue,
            "total_expenses": self.total_expenses,
            "net_income": self.net_income,
            "status": self.status,
            "generated_by": self.generated_by,
            "generated_at": self.generated_at,
            "approved_by": self.approved_by,
            "approved_at": self.approved_at,
            "notes": self.notes,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "FinancialReportModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            report_type=data.get("report_type"),
            title=data.get("title"),
            period_start=data.get("period_start"),
            period_end=data.get("period_end"),
            currency=data.get("currency", "XOF"),
            total_revenue=data.get("total_revenue", 0),
            total_expenses=data.get("total_expenses", 0),
            net_income=data.get("net_income", 0),
            status=data.get("status", "brouillon"),
            generated_by=data.get("generated_by"),
            generated_at=data.get("generated_at"),
            approved_by=data.get("approved_by"),
            approved_at=data.get("approved_at"),
            notes=data.get("notes"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def calculate_net_income(self):
        """Calcule le revenu net"""
        self.net_income = self.total_revenue - self.total_expenses
    
    def profit_margin(self) -> float:
        """Calcule la marge bénéficiaire"""
        if self.total_revenue == 0:
            return 0
        return (self.net_income / self.total_revenue) * 100
    
    def is_profitable(self) -> bool:
        """Vérifie si rentable"""
        return self.net_income > 0


class BalanceSheetModel:
    """Modèle de bilan"""
    
    def __init__(
        self,
        id: int,
        report_date: date,
        currency: str = "XOF",
        total_assets: float = 0,
        total_liabilities: float = 0,
        total_equity: float = 0,
        current_assets: float = 0,
        fixed_assets: float = 0,
        current_liabilities: float = 0,
        long_term_liabilities: float = 0,
        status: str = "brouillon",
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.report_date = report_date
        self.currency = currency
        self.total_assets = total_assets
        self.total_liabilities = total_liabilities
        self.total_equity = total_equity
        self.current_assets = current_assets
        self.fixed_assets = fixed_assets
        self.current_liabilities = current_liabilities
        self.long_term_liabilities = long_term_liabilities
        self.status = status
        self.notes = notes
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "report_date": self.report_date,
            "currency": self.currency,
            "total_assets": self.total_assets,
            "total_liabilities": self.total_liabilities,
            "total_equity": self.total_equity,
            "current_assets": self.current_assets,
            "fixed_assets": self.fixed_assets,
            "current_liabilities": self.current_liabilities,
            "long_term_liabilities": self.long_term_liabilities,
            "status": self.status,
            "notes": self.notes,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    def calculate_equity(self):
        """Calcule les capitaux propres"""
        self.total_equity = self.total_assets - self.total_liabilities
    
    def current_ratio(self) -> float:
        """Calcule le ratio de liquidité"""
        if self.current_liabilities == 0:
            return 0
        return self.current_assets / self.current_liabilities
    
    def debt_ratio(self) -> float:
        """Calcule le ratio d'endettement"""
        if self.total_assets == 0:
            return 0
        return (self.total_liabilities / self.total_assets) * 100


class CashFlowModel:
    """Modèle de flux de trésorerie"""
    
    def __init__(
        self,
        id: int,
        period_start: date,
        period_end: date,
        currency: str = "XOF",
        opening_balance: float = 0,
        cash_inflows: float = 0,
        cash_outflows: float = 0,
        closing_balance: float = 0,
        operating_cash_flow: float = 0,
        investing_cash_flow: float = 0,
        financing_cash_flow: float = 0,
        status: str = "brouillon",
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.period_start = period_start
        self.period_end = period_end
        self.currency = currency
        self.opening_balance = opening_balance
        self.cash_inflows = cash_inflows
        self.cash_outflows = cash_outflows
        self.closing_balance = closing_balance
        self.operating_cash_flow = operating_cash_flow
        self.investing_cash_flow = investing_cash_flow
        self.financing_cash_flow = financing_cash_flow
        self.status = status
        self.notes = notes
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "period_start": self.period_start,
            "period_end": self.period_end,
            "currency": self.currency,
            "opening_balance": self.opening_balance,
            "cash_inflows": self.cash_inflows,
            "cash_outflows": self.cash_outflows,
            "closing_balance": self.closing_balance,
            "operating_cash_flow": self.operating_cash_flow,
            "investing_cash_flow": self.investing_cash_flow,
            "financing_cash_flow": self.financing_cash_flow,
            "status": self.status,
            "notes": self.notes,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    def calculate_closing_balance(self):
        """Calcule le solde de clôture"""
        self.closing_balance = (self.opening_balance + 
                                self.cash_inflows - self.cash_outflows)
    
    def net_cash_flow(self) -> float:
        """Calcule le flux net"""
        return self.cash_inflows - self.cash_outflows
