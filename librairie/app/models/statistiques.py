"""
Modèle de données pour les statistiques de librairie

Ce module définit le modèle de données pour les statistiques
dans le module de gestion de librairie.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime, date
from typing import Optional


class CirculationStatsModel:
    """Modèle de statistiques de circulation"""
    
    def __init__(
        self,
        id: int,
        date: date = None,
        total_borrows: int = 0,
        total_returns: int = 0,
        total_renewals: int = 0,
        late_returns: int = 0,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.date = date
        self.total_borrows = total_borrows
        self.total_returns = total_returns
        self.total_renewals = total_renewals
        self.late_returns = late_returns
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "date": self.date,
            "total_borrows": self.total_borrows,
            "total_returns": self.total_returns,
            "total_renewals": self.total_renewals,
            "late_returns": self.late_returns,
            "created_at": self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "CirculationStatsModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            date=data.get("date"),
            total_borrows=data.get("total_borrows", 0),
            total_returns=data.get("total_returns", 0),
            total_renewals=data.get("total_renewals", 0),
            late_returns=data.get("late_returns", 0),
            created_at=data.get("created_at")
        )
    
    def return_rate(self) -> float:
        """Taux de retour"""
        if self.total_borrows == 0:
            return 0
        return (self.total_returns / self.total_borrows) * 100
    
    def late_rate(self) -> float:
        """Taux de retard"""
        if self.total_returns == 0:
            return 0
        return (self.late_returns / self.total_returns) * 100


class PopularBookModel:
    """Modèle de livre populaire"""
    
    def __init__(
        self,
        id: int,
        book_id: int,
        borrow_count: int = 0,
        period: str = "monthly",
        period_start: date = None,
        period_end: date = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.book_id = book_id
        self.borrow_count = borrow_count
        self.period = period
        self.period_start = period_start
        self.period_end = period_end
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "book_id": self.book_id,
            "borrow_count": self.borrow_count,
            "period": self.period,
            "period_start": self.period_start,
            "period_end": self.period_end,
            "created_at": self.created_at
        }


class MemberActivityModel:
    """Modèle d'activité de membre"""
    
    def __init__(
        self,
        id: int,
        member_id: int,
        date: date = None,
        borrows: int = 0,
        returns: int = 0,
        logins: int = 0,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.member_id = member_id
        self.date = date
        self.borrows = borrows
        self.returns = returns
        self.logins = logins
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "member_id": self.member_id,
            "date": self.date,
            "borrows": self.borrows,
            "returns": self.returns,
            "logins": self.logins,
            "created_at": self.created_at
        }
    
    def total_activities(self) -> int:
        """Total des activités"""
        return self.borrows + self.returns + self.logins
