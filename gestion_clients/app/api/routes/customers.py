"""
API Routes pour les clients

Ce module définit les routes API pour la gestion des clients.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from datetime import datetime


router = APIRouter(prefix="/clients", tags=["clients"])


# Mock data pour les tests
MOCK_CLIENTS = [
    {
        "id": 1,
        "name": "Entreprise SARL",
        "email": "contact@entreprise.sn",
        "phone": "+221771234567",
        "address": "Dakar, Sénégal",
        "client_type": "entreprise",
        "company": "Entreprise SARL",
        "contact_person": "M. Diop",
        "status": "actif",
        "total_revenue": 5000000,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
]


@router.get("/")
async def get_clients(
    client_type: str = None,
    status: str = None,
    search: str = None
):
    """Récupère la liste des clients"""
    clients = MOCK_CLIENTS
    
    if client_type:
        clients = [c for c in clients if c["client_type"] == client_type]
    if status:
        clients = [c for c in clients if c["status"] == status]
    if search:
        clients = [c for c in clients if search.lower() in c["name"].lower()]
    
    return {"clients": clients, "total": len(clients)}


@router.get("/{client_id}")
async def get_client(client_id: int):
    """Récupère un client par son ID"""
    for client in MOCK_CLIENTS:
        if client["id"] == client_id:
            return client
    
    raise HTTPException(status_code=404, detail="Client non trouvé")


@router.post("/")
async def create_client(client_data: dict):
    """Crée un nouveau client"""
    new_client = {
        "id": len(MOCK_CLIENTS) + 1,
        **client_data,
        "status": "actif",
        "total_revenue": 0,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
    MOCK_CLIENTS.append(new_client)
    return new_client


@router.put("/{client_id}")
async def update_client(client_id: int, client_data: dict):
    """Met à jour un client"""
    for i, client in enumerate(MOCK_CLIENTS):
        if client["id"] == client_id:
            MOCK_CLIENTS[i] = {
                **client,
                **client_data,
                "updated_at": datetime.now()
            }
            return MOCK_CLIENTS[i]
    
    raise HTTPException(status_code=404, detail="Client non trouvé")


@router.delete("/{client_id}")
async def delete_client(client_id: int):
    """Supprime un client"""
    for i, client in enumerate(MOCK_CLIENTS):
        if client["id"] == client_id:
            MOCK_CLIENTS.pop(i)
            return {"message": "Client supprimé"}
    
    raise HTTPException(status_code=404, detail="Client non trouvé")


@router.get("/{client_id}/orders")
async def get_client_orders(client_id: int):
    """Récupère les commandes d'un client"""
    return {"orders": [], "total": 0}


@router.get("/{client_id}/interactions")
async def get_client_interactions(client_id: int):
    """Récupère les interactions d'un client"""
    return {"interactions": [], "total": 0}


@router.post("/{client_id}/interactions")
async def create_interaction(client_id: int, interaction_data: dict):
    """Crée une interaction"""
    return {
        "id": 1,
        "client_id": client_id,
        **interaction_data,
        "created_at": datetime.now()
    }


# Routes pour les prospects (leads)
MOCK_LEADS = []


@router.get("/leads/")
async def get_leads(
    source: str = None,
    status: str = None,
    assigned_to: int = None
):
    """Récupère la liste des prospects"""
    leads = MOCK_LEADS
    
    if source:
        leads = [l for l in leads if l["source"] == source]
    if status:
        leads = [l for l in leads if l["status"] == status]
    if assigned_to:
        leads = [l for l in leads if l.get("assigned_to") == assigned_to]
    
    return {"leads": leads, "total": len(leads)}


@router.post("/leads/")
async def create_lead(lead_data: dict):
    """Crée un nouveau prospect"""
    new_lead = {
        "id": len(MOCK_LEADS) + 1,
        **lead_data,
        "status": "nouveau",
        "score": 0,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
    MOCK_LEADS.append(new_lead)
    return new_lead


@router.put("/leads/{lead_id}")
async def update_lead(lead_id: int, lead_data: dict):
    """Met à jour un prospect"""
    for i, lead in enumerate(MOCK_LEADS):
        if lead["id"] == lead_id:
            MOCK_LEADS[i] = {
                **lead,
                **lead_data,
                "updated_at": datetime.now()
            }
            return MOCK_LEADS[i]
    
    raise HTTPException(status_code=404, detail="Prospect non trouvé")
