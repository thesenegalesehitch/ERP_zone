"""
API Routes pour les tickets

Ce module définit les routes API pour la gestion des tickets de support.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from datetime import datetime


router = APIRouter(prefix="/tickets", tags=["tickets"])


# Mock data pour les tests
MOCK_TICKETS = [
    {
        "id": 1,
        "subject": "Problème de connexion",
        "description": "Impossible de se connecter au système",
        "ticket_type": "incident",
        "priority": "haute",
        "category": "technique",
        "status": "en_cours",
        "client_id": 1,
        "assigned_to": 1,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
]


@router.get("/")
async def get_tickets(
    status: str = None,
    priority: str = None,
    category: str = None,
    assigned_to: int = None
):
    """Récupère la liste des tickets"""
    tickets = MOCK_TICKETS
    
    if status:
        tickets = [t for t in tickets if t["status"] == status]
    if priority:
        tickets = [t for t in tickets if t["priority"] == priority]
    if category:
        tickets = [t for t in tickets if t["category"] == category]
    if assigned_to:
        tickets = [t for t in tickets if t.get("assigned_to") == assigned_to]
    
    return {"tickets": tickets, "total": len(tickets)}


@router.get("/{ticket_id}")
async def get_ticket(ticket_id: int):
    """Récupère un ticket par son ID"""
    for ticket in MOCK_TICKETS:
        if ticket["id"] == ticket_id:
            return ticket
    
    raise HTTPException(status_code=404, detail="Ticket non trouvé")


@router.post("/")
async def create_ticket(ticket_data: dict):
    """Crée un nouveau ticket"""
    new_ticket = {
        "id": len(MOCK_TICKETS) + 1,
        **ticket_data,
        "status": "nouveau",
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
    MOCK_TICKETS.append(new_ticket)
    return new_ticket


@router.put("/{ticket_id}")
async def update_ticket(ticket_id: int, ticket_data: dict):
    """Met à jour un ticket"""
    for i, ticket in enumerate(MOCK_TICKETS):
        if ticket["id"] == ticket_id:
            MOCK_TICKETS[i] = {
                **ticket,
                **ticket_data,
                "updated_at": datetime.now()
            }
            return MOCK_TICKETS[i]
    
    raise HTTPException(status_code=404, detail="Ticket non trouvé")


@router.post("/{ticket_id}/comments")
async def add_comment(ticket_id: int, comment_data: dict):
    """Ajoute un commentaire"""
    return {
        "id": 1,
        "ticket_id": ticket_id,
        **comment_data,
        "created_at": datetime.now()
    }


@router.get("/{ticket_id}/comments")
async def get_comments(ticket_id: int):
    """Récupère les commentaires d'un ticket"""
    return {"comments": [], "total": 0}


# Routes pour la base de connaissances
MOCK_ARTICLES = []


@router.get("/knowledge-base/")
async def get_kb_articles(category: str = None):
    """Récupère les articles de la base de connaissances"""
    articles = MOCK_ARTICLES
    
    if category:
        articles = [a for a in articles if a.get("category") == category]
    
    return {"articles": articles, "total": len(articles)}


@router.get("/knowledge-base/{article_id}")
async def get_kb_article(article_id: int):
    """Récupère un article par son ID"""
    for article in MOCK_ARTICLES:
        if article["id"] == article_id:
            return article
    
    raise HTTPException(status_code=404, detail="Article non trouvé")


@router.post("/knowledge-base/")
async def create_kb_article(article_data: dict):
    """Crée un nouvel article"""
    new_article = {
        "id": len(MOCK_ARTICLES) + 1,
        **article_data,
        "is_published": False,
        "views": 0,
        "helpful_count": 0,
        "created_at": datetime.now()
    }
    MOCK_ARTICLES.append(new_article)
    return new_article


@router.get("/stats")
async def get_support_stats():
    """Récupère les statistiques du support"""
    return {
        "total_tickets": len(MOCK_TICKETS),
        "open_tickets": sum(1 for t in MOCK_TICKETS if t["status"] in ["nouveau", "en_cours"]),
        "resolved_tickets": sum(1 for t in MOCK_TICKETS if t["status"] == "resolu"),
        "avg_resolution_time": 0
    }
