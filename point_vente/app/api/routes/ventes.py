"""
API Routes pour les ventes

Ce module définit les routes API pour la gestion des ventes.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from datetime import datetime


router = APIRouter(prefix="/ventes", tags=["point_vente"])


# Mock data pour les tests
MOCK_SALES = [
    {
        "id": 1,
        "items": [
            {"product_id": 1, "quantity": 2, "unit_price": 5000, "discount": 0}
        ],
        "subtotal": 10000,
        "tax_amount": 1800,
        "discount": 0,
        "total": 11800,
        "paid_amount": 12000,
        "change_amount": 200,
        "status": "terminee",
        "payment_method": "especes",
        "sale_type": "comptoir",
        "cashier_id": 1,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
]


@router.get("/")
async def get_sales(
    status: str = None,
    payment_method: str = None,
    sale_type: str = None,
    cashier_id: int = None
):
    """Récupère la liste des ventes"""
    sales = MOCK_SALES
    
    if status:
        sales = [s for s in sales if s["status"] == status]
    if payment_method:
        sales = [s for s in sales if s["payment_method"] == payment_method]
    if sale_type:
        sales = [s for s in sales if s["sale_type"] == sale_type]
    if cashier_id:
        sales = [s for s in sales if s["cashier_id"] == cashier_id]
    
    return {"sales": sales, "total": len(sales)}


@router.get("/{sale_id}")
async def get_sale(sale_id: int):
    """Récupère une vente par son ID"""
    for sale in MOCK_SALES:
        if sale["id"] == sale_id:
            return sale
    
    raise HTTPException(status_code=404, detail="Vente non trouvée")


@router.post("/")
async def create_sale(sale_data: dict):
    """Crée une nouvelle vente"""
    subtotal = sum(
        item["quantity"] * item["unit_price"]
        for item in sale_data.get("items", [])
    )
    tax_amount = subtotal * 0.18
    total = subtotal + tax_amount - sale_data.get("discount", 0)
    
    new_sale = {
        "id": len(MOCK_SALES) + 1,
        **sale_data,
        "subtotal": subtotal,
        "tax_amount": tax_amount,
        "discount": sale_data.get("discount", 0),
        "total": total,
        "status": "terminee",
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
    MOCK_SALES.append(new_sale)
    return new_sale


@router.post("/{sale_id}/cancel")
async def cancel_sale(sale_id: int):
    """Annule une vente"""
    for i, sale in enumerate(MOCK_SALES):
        if sale["id"] == sale_id:
            MOCK_SALES[i]["status"] = "annulee"
            return MOCK_SALES[i]
    
    raise HTTPException(status_code=404, detail="Vente non trouvée")


# Routes pour les tables
MOCK_TABLES = [
    {"id": 1, "table_number": "T1", "capacity": 4, "section": "Terrasse", "status": "disponible"},
    {"id": 2, "table_number": "T2", "capacity": 4, "section": "Terrasse", "status": "occupyee"}
]


@router.get("/tables/")
async def get_tables(status: str = None):
    """Récupère la liste des tables"""
    tables = MOCK_TABLES
    
    if status:
        tables = [t for t in tables if t["status"] == status]
    
    return {"tables": tables, "total": len(tables)}


@router.get("/tables/{table_id}")
async def get_table(table_id: int):
    """Récupère une table par son ID"""
    for table in MOCK_TABLES:
        if table["id"] == table_id:
            return table
    
    raise HTTPException(status_code=404, detail="Table non trouvée")


# Routes pour les rapports
@router.get("/quotidien")
async def get_daily_report(date: datetime = None):
    """Récupère le rapport quotidien"""
    return {
        "date": date or datetime.now(),
        "total_sales": len(MOCK_SALES),
        "total_revenue": sum(s["total"] for s in MOCK_SALES),
        "average_sale": sum(s["total"] for s in MOCK_SALES) / len(MOCK_SALES) if MOCK_SALES else 0,
        "items_sold": sum(
            sum(item["quantity"] for item in s["items"])
            for s in MOCK_SALES
        )
    }


@router.get("/produits-populaires")
async def get_popular_products(limit: int = 10):
    """Récupère les produits populaires"""
    return {"products": [], "total": 0}
