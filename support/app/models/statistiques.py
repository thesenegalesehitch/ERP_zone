"""
Modèle de données pour les statistiques

Ce module définit le modèle de données pour les statistiques
dans le module de support.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime, date
from typing import Optional


class TicketStatsModel:
    """Modèle de statistiques de ticket"""
    
    def __init__(
        self,
        id: int,
        date: date,
        total_tickets: int = 0,
        open_tickets: int = 0,
        closed_tickets: int = 0,
        pending_tickets: int = 0,
        avg_response_time: float = 0,
        avg_resolution_time: float = 0,
        customer_satisfaction: float = 0,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.date = date
        self.total_tickets = total_tickets
        self.open_tickets = open_tickets
        self.closed_tickets = closed_tickets
        self.pending_tickets = pending_tickets
        self.avg_response_time = avg_response_time
        self.avg_resolution_time = avg_resolution_time
        self.customer_satisfaction = customer_satisfaction
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "date": self.date,
            "total_tickets": self.total_tickets,
            "open_tickets": self.open_tickets,
            "closed_tickets": self.closed_tickets,
            "pending_tickets": self.pending_tickets,
            "avg_response_time": self.avg_response_time,
            "avg_resolution_time": self.avg_resolution_time,
            "customer_satisfaction": self.customer_satisfaction,
            "created_at": self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "TicketStatsModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            date=data.get("date"),
            total_tickets=data.get("total_tickets", 0),
            open_tickets=data.get("open_tickets", 0),
            closed_tickets=data.get("closed_tickets", 0),
            pending_tickets=data.get("pending_tickets", 0),
            avg_response_time=data.get("avg_response_time", 0),
            avg_resolution_time=data.get("avg_resolution_time", 0),
            customer_satisfaction=data.get("customer_satisfaction", 0),
            created_at=data.get("created_at")
        )


class AgentPerformanceModel:
    """Modèle de performance d'agent"""
    
    def __init__(
        self,
        id: int,
        agent_id: int,
        date: date,
        tickets_handled: int = 0,
        tickets_resolved: int = 0,
        avg_response_time: float = 0,
        avg_resolution_time: float = 0,
        customer_rating: float = 0,
        first_contact_resolution: float = 0,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.agent_id = agent_id
        self.date = date
        self.tickets_handled = tickets_handled
        self.tickets_resolved = tickets_resolved
        self.avg_response_time = avg_response_time
        self.avg_resolution_time = avg_resolution_time
        self.customer_rating = customer_rating
        self.first_contact_resolution = first_contact_resolution
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "agent_id": self.agent_id,
            "date": self.date,
            "tickets_handled": self.tickets_handled,
            "tickets_resolved": self.tickets_resolved,
            "avg_response_time": self.avg_response_time,
            "avg_resolution_time": self.avg_resolution_time,
            "customer_rating": self.customer_rating,
            "first_contact_resolution": self.first_contact_resolution,
            "created_at": self.created_at
        }
    
    def resolution_rate(self) -> float:
        """Calcule le taux de résolution"""
        if self.tickets_handled == 0:
            return 0
        return (self.tickets_resolved / self.tickets_handled) * 100


class KnowledgeBaseStatsModel:
    """Modèle de statistiques de base de connaissances"""
    
    def __init__(
        self,
        id: int,
        date: date,
        total_articles: int = 0,
        total_views: int = 0,
        total_searches: int = 0,
        successful_searches: int = 0,
        avg_time_on_page: float = 0,
        helpful_votes: int = 0,
        not_helpful_votes: int = 0,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.date = date
        self.total_articles = total_articles
        self.total_views = total_views
        self.total_searches = total_searches
        self.successful_searches = successful_searches
        self.avg_time_on_page = avg_time_on_page
        self.helpful_votes = helpful_votes
        self.not_helpful_votes = not_helpful_votes
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "date": self.date,
            "total_articles": self.total_articles,
            "total_views": self.total_views,
            "total_searches": self.total_searches,
            "successful_searches": self.successful_searches,
            "avg_time_on_page": self.avg_time_on_page,
            "helpful_votes": self.helpful_votes,
            "not_helpful_votes": self.not_helpful_votes,
            "created_at": self.created_at
        }
    
    def search_success_rate(self) -> float:
        """Calcule le taux de recherche réussie"""
        if self.total_searches == 0:
            return 0
        return (self.successful_searches / self.total_searches) * 100
    
    def helpfulness_ratio(self) -> float:
        """Calcule le ratio d'utilité"""
        total = self.helpful_votes + self.not_helpful_votes
        if total == 0:
            return 0
        return (self.helpful_votes / total) * 100
