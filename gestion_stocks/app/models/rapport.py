"""
Modèle de données pour les rapports de stock

Ce module définit le modèle de données pour les rapports
dans le module de gestion des stocks.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime, date
from typing import Optional


class StockReportModel:
    """Modèle de rapport de stock"""
    
    def __init__(
        self,
        id: int,
        report_type: str,
        warehouse_id: Optional[int] = None,
        category_id: Optional[int] = None,
        report_date: Optional[date] = None,
        status: str = "genere",
        total_products: int = 0,
        total_value: float = 0,
        low_stock_count: int = 0,
        out_of_stock_count: int = 0,
        file_path: Optional[str] = None,
        generated_by: int = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.report_type = report_type
        self.warehouse_id = warehouse_id
        self.category_id = category_id
        self.report_date = report_date
        self.status = status
        self.total_products = total_products
        self.total_value = total_value
        self.low_stock_count = low_stock_count
        self.out_of_stock_count = out_of_stock_count
        self.file_path = file_path
        self.generated_by = generated_by
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "report_type": self.report_type,
            "warehouse_id": self.warehouse_id,
            "category_id": self.category_id,
            "report_date": self.report_date,
            "status": self.status,
            "total_products": self.total_products,
            "total_value": self.total_value,
            "low_stock_count": self.low_stock_count,
            "out_of_stock_count": self.out_of_stock_count,
            "file_path": self.file_path,
            "generated_by": self.generated_by,
            "created_at": self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "StockReportModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            report_type=data.get("report_type"),
            warehouse_id=data.get("warehouse_id"),
            category_id=data.get("category_id"),
            report_date=data.get("report_date"),
            status=data.get("status", "genere"),
            total_products=data.get("total_products", 0),
            total_value=data.get("total_value", 0),
            low_stock_count=data.get("low_stock_count", 0),
            out_of_stock_count=data.get("out_of_stock_count", 0),
            file_path=data.get("file_path"),
            generated_by=data.get("generated_by"),
            created_at=data.get("created_at")
        )


class StockValuationModel:
    """Modèle d'évaluation de stock"""
    
    def __init__(
        self,
        id: int,
        warehouse_id: int,
        valuation_date: date,
        total_cost: float = 0,
        total_retail: float = 0,
        item_count: int = 0,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.warehouse_id = warehouse_id
        self.valuation_date = valuation_date
        self.total_cost = total_cost
        self.total_retail = total_retail
        self.item_count = item_count
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "warehouse_id": self.warehouse_id,
            "valuation_date": self.valuation_date,
            "total_cost": self.total_cost,
            "total_retail": self.total_retail,
            "item_count": self.item_count,
            "created_at": self.created_at
        }
    
    def potential_profit(self) -> float:
        """Calcule le profit potentiel"""
        return self.total_retail - self.total_cost


class ReorderReportModel:
    """Modèle de rapport de réapprovisionnement"""
    
    def __init__(
        self,
        id: int,
        product_id: int,
        warehouse_id: int,
        current_stock: int = 0,
        reorder_point: int = 0,
        suggested_quantity: int = 0,
        last_reorder_date: Optional[date] = None,
        supplier_id: Optional[int] = None,
        status: str = "en_attente",
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.product_id = product_id
        self.warehouse_id = warehouse_id
        self.current_stock = current_stock
        self.reorder_point = reorder_point
        self.suggested_quantity = suggested_quantity
        self.last_reorder_date = last_reorder_date
        self.supplier_id = supplier_id
        self.status = status
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "product_id": self.product_id,
            "warehouse_id": self.warehouse_id,
            "current_stock": self.current_stock,
            "reorder_point": self.reorder_point,
            "suggested_quantity": self.suggested_quantity,
            "last_reorder_date": self.last_reorder_date,
            "supplier_id": self.supplier_id,
            "status": self.status,
            "created_at": self.created_at
        }
    
    def needs_reorder(self) -> bool:
        """Vérifie si un réapprovisionnement est nécessaire"""
        return self.current_stock <= self.reorder_point


class StockMovementReportModel:
    """Modèle de rapport de mouvement de stock"""
    
    def __init__(
        self,
        id: int,
        product_id: int,
        warehouse_id: int,
        movement_type: str,
        quantity: int,
        balance_before: int = 0,
        balance_after: int = 0,
        reference: Optional[str] = None,
        movement_date: Optional[datetime] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.product_id = product_id
        self.warehouse_id = warehouse_id
        self.movement_type = movement_type
        self.quantity = quantity
        self.balance_before = balance_before
        self.balance_after = balance_after
        self.reference = reference
        self.movement_date = movement_date or datetime.now()
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "product_id": self.product_id,
            "warehouse_id": self.warehouse_id,
            "movement_type": self.movement_type,
            "quantity": self.quantity,
            "balance_before": self.balance_before,
            "balance_after": self.balance_after,
            "reference": self.reference,
            "movement_date": self.movement_date,
            "created_at": self.created_at
        }
