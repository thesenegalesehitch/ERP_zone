"""
API Routes pour les commandes

Ce module définit les routes API pour la gestion des commandes de restaurant.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from datetime import datetime


router = APIRouter(prefix="/commandes", tags=["restaurant"])


# Mock data pour les tests
MOCK_ORDERS = [
    {
        "id": 1,
        "table_id": 1,
        "items": [
            {"menu_item_id": 1, "quantity": 2, "notes": ""}
        ],
        "subtotal": 10000,
        "tax_amount": 1800,
        "total": 11800,
        "status": "servie",
        "order_type": "sur_place",
        "waiter_id": 1,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
]


@router.get("/")
async def get_orders(
    status: str = None,
    order_type: str = None,
    table_id: int = None,
    waiter_id: int = None
):
    """Récupère la liste des commandes"""
    orders = MOCK_ORDERS
    
    if status:
        orders = [o for o in orders if o["status"] == status]
    if order_type:
        orders = [o for o in orders if o["order_type"] == order_type]
    if table_id:
        orders = [o for o in orders if o.get("table_id") == table_id]
    if waiter_id:
        orders = [o for o in orders if o["waiter_id"] == waiter_id]
    
    return {"orders": orders, "total": len(orders)}


@router.get("/{order_id}")
async def get_order(order_id: int):
    """Récupère une commande par son ID"""
    for order in MOCK_ORDERS:
        if order["id"] == order_id:
            return order
    
    raise HTTPException(status_code=404, detail="Commande non trouvée")


@router.post("/")
async def create_order(order_data: dict):
    """Crée une nouvelle commande"""
    subtotal = sum(
        item["quantity"] * item.get("price", 0)
        for item in order_data.get("items", [])
    )
    tax_amount = subtotal * 0.18
    total = subtotal + tax_amount
    
    new_order = {
        "id": len(MOCK_ORDERS) + 1,
        **order_data,
        "subtotal": subtotal,
        "tax_amount": tax_amount,
        "total": total,
        "status": "en_attente",
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
    MOCK_ORDERS.append(new_order)
    return new_order


@router.put("/{order_id}")
async def update_order(order_id: int, order_data: dict):
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


@router.post("/{order_id}/send-to-kitchen")
async def send_to_kitchen(order_id: int):
    """Envoie la commande en cuisine"""
    for i, order in enumerate(MOCK_ORDERS):
        if order["id"] == order_id:
            MOCK_ORDERS[i]["status"] = "en_preparation"
            return MOCK_ORDERS[i]
    
    raise HTTPException(status_code=404, detail="Commande non trouvée")


# Routes pour le menu
MOCK_MENU_ITEMS = [
    {"id": 1, "name": "Poulet DG", "price": 5000, "category": "plat_principal", "available": True},
    {"id": 2, "name": "Thieboudienne", "price": 3500, "category": "plat_principal", "available": True}
]


@router.get("/menu/")
async def get_menu_items(category: str = None):
    """Récupère les articles du menu"""
    items = MOCK_MENU_ITEMS
    
    if category:
        items = [m for m in items if m["category"] == category]
    
    return {"items": items, "total": len(items)}


# Routes pour les tables
MOCK_TABLES = [
    {"id": 1, "table_number": "T1", "capacity": 4, "section": "Salle", "status": "occupyee"},
    {"id": 2, "table_number": "T2", "capacity": 4, "section": "Salle", "status": "disponible"}
]


@router.get("/tables/")
async def get_tables(status: str = None):
    """Récupère la liste des tables"""
    tables = MOCK_TABLES
    
    if status:
        tables = [t for t in tables if t["status"] == status]
    
    return {"tables": tables, "total": len(tables)}


# Routes pour les réservations
MOCK_RESERVATIONS = []


@router.get("/reservations/")
async def get_reservations(date: datetime = None):
    """Récupère les réservations"""
    reservations = MOCK_RESERVATIONS
    
    if date:
        reservations = [r for r in reservations if r["reservation_date"].date() == date.date()]
    
    return {"reservations": reservations, "total": len(reservations)}


@router.post("/reservations/")
async def create_reservation(reservation_data: dict):
    """Crée une réservation"""
    new_reservation = {
        "id": len(MOCK_RESERVATIONS) + 1,
        **reservation_data,
        "status": "confirmee",
        "created_at": datetime.now()
    }
    MOCK_RESERVATIONS.append(new_reservation)
    return new_reservation
