"""
API Routes pour les produits

Ce module définit les routes API pour la gestion des produits.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from datetime import datetime


router = APIRouter(prefix="/products", tags=["products"])


# Mock data pour les tests
MOCK_PRODUCTS = [
    {
        "id": 1,
        "name": "Ordinateur Portable",
        "description": "PC Portable 15 pouces",
        "sku": "PC-001",
        "barcode": "1234567890123",
        "category": "informatique",
        "unit_price": 350000,
        "cost_price": 280000,
        "quantity": 25,
        "reorder_point": 10,
        "warehouse_id": 1,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
]


@router.get("/")
async def get_products(
    category: str = None,
    warehouse_id: int = None,
    low_stock: bool = None,
    search: str = None
):
    """Récupère la liste des produits"""
    products = MOCK_PRODUCTS
    
    if category:
        products = [p for p in products if p["category"] == category]
    if warehouse_id:
        products = [p for p in products if p.get("warehouse_id") == warehouse_id]
    if low_stock:
        products = [p for p in products if p["quantity"] <= p["reorder_point"]]
    if search:
        products = [p for p in products if search.lower() in p["name"].lower()]
    
    return {"products": products, "total": len(products)}


@router.get("/{product_id}")
async def get_product(product_id: int):
    """Récupère un produit par son ID"""
    for product in MOCK_PRODUCTS:
        if product["id"] == product_id:
            return product
    
    raise HTTPException(status_code=404, detail="Produit non trouvé")


@router.post("/")
async def create_product(product_data: dict):
    """Crée un nouveau produit"""
    new_product = {
        "id": len(MOCK_PRODUCTS) + 1,
        **product_data,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
    MOCK_PRODUCTS.append(new_product)
    return new_product


@router.put("/{product_id}")
async def update_product(product_id: int, product_data: dict):
    """Met à jour un produit"""
    for i, product in enumerate(MOCK_PRODUCTS):
        if product["id"] == product_id:
            MOCK_PRODUCTS[i] = {
                **product,
                **product_data,
                "updated_at": datetime.now()
            }
            return MOCK_PRODUCTS[i]
    
    raise HTTPException(status_code=404, detail="Produit non trouvé")


@router.delete("/{product_id}")
async def delete_product(product_id: int):
    """Supprime un produit"""
    for i, product in enumerate(MOCK_PRODUCTS):
        if product["id"] == product_id:
            MOCK_PRODUCTS.pop(i)
            return {"message": "Produit supprimé"}
    
    raise HTTPException(status_code=404, detail="Produit non trouvé")


@router.post("/{product_id}/movements")
async def create_stock_movement(product_id: int, movement_data: dict):
    """Crée un mouvement de stock"""
    return {
        "id": 1,
        "product_id": product_id,
        **movement_data,
        "created_at": datetime.now()
    }


@router.get("/{product_id}/movements")
async def get_stock_movements(product_id: int):
    """Récupère les mouvements de stock"""
    return {"movements": [], "total": 0}


@router.post("/{product_id}/adjust")
async def adjust_stock(product_id: int, adjustment_data: dict):
    """Ajuste le stock"""
    return {
        "id": 1,
        "product_id": product_id,
        **adjustment_data,
        "adjusted_at": datetime.now()
    }


@router.get("/low-stock/alerts")
async def get_low_stock_alerts():
    """Récupère les alertes de stock bas"""
    low_stock_products = [p for p in MOCK_PRODUCTS if p["quantity"] <= p["reorder_point"]]
    return {"alerts": low_stock_products, "total": len(low_stock_products)}
