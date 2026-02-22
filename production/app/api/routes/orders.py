"""
API Routes pour les ordres de fabrication

Ce module définit les routes API pour la gestion de la production.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from datetime import datetime


router = APIRouter(prefix="/orders", tags=["production"])


# Mock data pour les tests
MOCK_ORDERS = [
    {
        "id": 1,
        "product_id": 1,
        "quantity": 100,
        "priority": "normale",
        "status": "en_cours",
        "estimated_hours": 40,
        "actual_hours": 20,
        "started_at": datetime.now(),
        "due_date": None,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
]


@router.get("/")
async def get_orders(
    status: str = None,
    priority: str = None,
    product_id: int = None
):
    """Récupère la liste des ordres de fabrication"""
    orders = MOCK_ORDERS
    
    if status:
        orders = [o for o in orders if o["status"] == status]
    if priority:
        orders = [o for o in orders if o["priority"] == priority]
    if product_id:
        orders = [o for o in orders if o["product_id"] == product_id]
    
    return {"orders": orders, "total": len(orders)}


@router.get("/{order_id}")
async def get_order(order_id: int):
    """Récupère un ordre de fabrication par son ID"""
    for order in MOCK_ORDERS:
        if order["id"] == order_id:
            return order
    
    raise HTTPException(status_code=404, detail="Ordre de fabrication non trouvé")


@router.post("/")
async def create_order(order_data: dict):
    """Crée un nouvel ordre de fabrication"""
    new_order = {
        "id": len(MOCK_ORDERS) + 1,
        **order_data,
        "status": "planifie",
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
    MOCK_ORDERS.append(new_order)
    return new_order


@router.put("/{order_id}")
async def update_order(order_id: int, order_data: dict):
    """Met à jour un ordre de fabrication"""
    for i, order in enumerate(MOCK_ORDERS):
        if order["id"] == order_id:
            MOCK_ORDERS[i] = {
                **order,
                **order_data,
                "updated_at": datetime.now()
            }
            return MOCK_ORDERS[i]
    
    raise HTTPException(status_code=404, detail="Ordre de fabrication non trouvé")


@router.post("/{order_id}/start")
async def start_order(order_id: int):
    """Démarre un ordre de fabrication"""
    for i, order in enumerate(MOCK_ORDERS):
        if order["id"] == order_id:
            MOCK_ORDERS[i]["status"] = "en_cours"
            MOCK_ORDERS[i]["started_at"] = datetime.now()
            return MOCK_ORDERS[i]
    
    raise HTTPException(status_code=404, detail="Ordre de fabrication non trouvé")


@router.post("/{order_id}/complete")
async def complete_order(order_id: int):
    """Termine un ordre de fabrication"""
    for i, order in enumerate(MOCK_ORDERS):
        if order["id"] == order_id:
            MOCK_ORDERS[i]["status"] = "termine"
            MOCK_ORDERS[i]["completed_at"] = datetime.now()
            return MOCK_ORDERS[i]
    
    raise HTTPException(status_code=404, detail="Ordre de fabrication non trouvé")


# Routes pour les postes de travail
MOCK_WORKSTATIONS = []


@router.get("/workstations/")
async def get_workstations():
    """Récupère la liste des postes de travail"""
    return {"workstations": MOCK_WORKSTATIONS, "total": 0}


@router.post("/workstations/")
async def create_workstation(workstation_data: dict):
    """Crée un poste de travail"""
    new_workstation = {
        "id": len(MOCK_WORKSTATIONS) + 1,
        **workstation_data,
        "status": "disponible",
        "created_at": datetime.now()
    }
    MOCK_WORKSTATIONS.append(new_workstation)
    return new_workstation


# Routes pour les контрол качества
MOCK_QUALITY_CHECKS = []


@router.get("/quality-checks/")
async def get_quality_checks(work_order_id: int = None):
    """Récupère les contrôles qualité"""
    checks = MOCK_QUALITY_CHECKS
    
    if work_order_id:
        checks = [c for c in checks if c.get("work_order_id") == work_order_id]
    
    return {"checks": checks, "total": len(checks)}


@router.post("/quality-checks/")
async def create_quality_check(check_data: dict):
    """Crée un contrôle qualité"""
    new_check = {
        "id": len(MOCK_QUALITY_CHECKS) + 1,
        **check_data,
        "defective_quantity": 0,
        "created_at": datetime.now()
    }
    MOCK_QUALITY_CHECKS.append(new_check)
    return new_check


@router.get("/stats")
async def get_production_stats():
    """Récupère les statistiques de production"""
    return {
        "total_orders": len(MOCK_ORDERS),
        "completed_orders": sum(1 for o in MOCK_ORDERS if o["status"] == "termine"),
        "in_progress_orders": sum(1 for o in MOCK_ORDERS if o["status"] == "en_cours"),
        "total_quantity": sum(o["quantity"] for o in MOCK_ORDERS),
        "defect_rate": 0
    }
