"""
API Routes pour les achats

Ce module définit les routes API pour la gestion des approvisionnements.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from datetime import datetime


router = APIRouter(prefix="/achats", tags=["achats"])


# Mock data pour les tests
MOCK_SUPPLIERS = [
    {
        "id": 1,
        "name": "Fournisseur.sn",
        "email": "contact@fournisseur.sn",
        "phone": "+221771234567",
        "address": "Dakar, Sénégal",
        "supplier_type": "distributeur",
        "contact_person": "M. Faye",
        "status": "actif",
        "rating": 4.5,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
]


@router.get("/fournisseurs/")
async def get_suppliers(
    supplier_type: str = None,
    status: str = None,
    search: str = None
):
    """Récupère la liste des fournisseurs"""
    suppliers = MOCK_SUPPLIERS
    
    if supplier_type:
        suppliers = [s for s in suppliers if s["supplier_type"] == supplier_type]
    if status:
        suppliers = [s for s in suppliers if s["status"] == status]
    if search:
        suppliers = [s for s in suppliers if search.lower() in s["name"].lower()]
    
    return {"suppliers": suppliers, "total": len(suppliers)}


@router.get("/fournisseurs/{supplier_id}")
async def get_supplier(supplier_id: int):
    """Récupère un fournisseur par son ID"""
    for supplier in MOCK_SUPPLIERS:
        if supplier["id"] == supplier_id:
            return supplier
    
    raise HTTPException(status_code=404, detail="Fournisseur non trouvé")


@router.post("/fournisseurs/")
async def create_supplier(supplier_data: dict):
    """Crée un nouveau fournisseur"""
    new_supplier = {
        "id": len(MOCK_SUPPLIERS) + 1,
        **supplier_data,
        "status": "actif",
        "rating": 0,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
    MOCK_SUPPLIERS.append(new_supplier)
    return new_supplier


# Routes pour les commandes
MOCK_ORDERS = []


@router.get("/commandes/")
async def get_purchase_orders(
    status: str = None,
    supplier_id: int = None,
    priority: str = None
):
    """Récupère la liste des commandes"""
    orders = MOCK_ORDERS
    
    if status:
        orders = [o for o in orders if o["status"] == status]
    if supplier_id:
        orders = [o for o in orders if o["supplier_id"] == supplier_id]
    if priority:
        orders = [o for o in orders if o["priority"] == priority]
    
    return {"orders": orders, "total": len(orders)}


@router.post("/commandes/")
async def create_purchase_order(order_data: dict):
    """Crée une nouvelle commande"""
    new_order = {
        "id": len(MOCK_ORDERS) + 1,
        **order_data,
        "status": "brouillon",
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
    MOCK_ORDERS.append(new_order)
    return new_order


@router.get("/commandes/{order_id}")
async def get_purchase_order(order_id: int):
    """Récupère une commande par son ID"""
    for order in MOCK_ORDERS:
        if order["id"] == order_id:
            return order
    
    raise HTTPException(status_code=404, detail="Commande non trouvée")


@router.put("/commandes/{order_id}")
async def update_purchase_order(order_id: int, order_data: dict):
    """Met à jour une commande"""
    for i, order in enumerate(MOCK_ORDERS):
        if order["id"] == order_id:
            MOCK_ORDERS[i] = {
                **order,
                **order_data,
                "updated_at": datetime.now()
            }
            return MOCK_ORDERS[i]
    
    raise HTTPException(status_code=404, detail="Commande non trouvée")


@router.post("/commandes/{order_id}/submit")
async def submit_purchase_order(order_id: int):
    """Soumet une commande"""
    for i, order in enumerate(MOCK_ORDERS):
        if order["id"] == order_id:
            MOCK_ORDERS[i]["status"] = "soumise"
            return MOCK_ORDERS[i]
    
    raise HTTPException(status_code=404, detail="Commande non trouvée")


@router.post("/commandes/{order_id}/receive")
async def receive_purchase_order(order_id: int, receipt_data: dict):
    """Reçoit une commande"""
    for i, order in enumerate(MOCK_ORDERS):
        if order["id"] == order_id:
            MOCK_ORDERS[i]["status"] = "recue"
            return MOCK_ORDERS[i]
    
    raise HTTPException(status_code=404, detail="Commande non trouvée")


@router.get("/stats")
async def get_purchasing_stats():
    """Récupère les statistiques d'achat"""
    return {
        "total_orders": len(MOCK_ORDERS),
        "pending_orders": sum(1 for o in MOCK_ORDERS if o["status"] == "soumise"),
        "received_orders": sum(1 for o in MOCK_ORDERS if o["status"] == "recue"),
        "total_suppliers": len(MOCK_SUPPLIERS)
    }
