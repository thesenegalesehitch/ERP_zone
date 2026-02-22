"""
Schémas de validation pour la production

Ce module définit les schémas Pydantic pour la validation
des données liées à la production.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class WorkOrderBase(BaseModel):
    """Schéma de base pour un ordre de fabrication"""
    product_id: int
    quantity: int = Field(..., gt=0)


class WorkOrderCreate(WorkOrderBase):
    """Schéma pour créer un ordre de fabrication"""
    priority: str = Field(default="normale")
    due_date: Optional[datetime] = None


class WorkOrderUpdate(BaseModel):
    """Schéma pour mettre à jour un ordre de fabrication"""
    status: Optional[str] = None
    priority: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


class WorkOrderResponse(WorkOrderBase):
    """Schéma pour la réponse d'un ordre de fabrication"""
    id: int
    priority: str
    status: str
    estimated_hours: Optional[float] = None
    actual_hours: Optional[float] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    due_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class BillOfMaterialsBase(BaseModel):
    """Schéma de base pour une nomenclature"""
    product_id: int


class BillOfMaterialsCreate(BillOfMaterialsBase):
    """Schéma pour créer une nomenclature"""
    materials: List[dict]


class BillOfMaterialsResponse(BillOfMaterialsBase):
    """Schéma pour la réponse d'une nomenclature"""
    id: int
    materials: List[dict]
    total_cost: float
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class QualityCheckCreate(BaseModel):
    """Schéma pour créer un contrôle qualité"""
    work_order_id: int
    check_type: str = Field(default="finale")
    quantity_checked: int = Field(..., gt=0)
    result: str
    notes: Optional[str] = None


class QualityCheckResponse(BaseModel):
    """Schéma pour la réponse d'un contrôle qualité"""
    id: int
    work_order_id: int
    check_type: str
    quantity_checked: int
    result: str
    defective_quantity: int = 0
    notes: Optional[str] = None
    checked_by: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class WorkStationBase(BaseModel):
    """Schéma de base pour un poste de travail"""
    name: str = Field(..., min_length=1, max_length=100)
    workstation_type: str


class WorkStationCreate(WorkStationBase):
    """Schéma pour créer un poste de travail"""
    capacity: Optional[int] = None
    hourly_cost: Optional[float] = None


class WorkStationUpdate(BaseModel):
    """Schéma pour mettre à jour un poste de travail"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    status: Optional[str] = None
    capacity: Optional[int] = None
    hourly_cost: Optional[float] = None


class WorkStationResponse(WorkStationBase):
    """Schéma pour la réponse d'un poste de travail"""
    id: int
    capacity: Optional[int] = None
    hourly_cost: Optional[float] = None
    status: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class WorkOrderFilter(BaseModel):
    """Schéma pour filtrer les ordres de fabrication"""
    status: Optional[str] = None
    priority: Optional[str] = None
    product_id: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class ProductionStats(BaseModel):
    """Schéma pour les statistiques de production"""
    total_orders: int
    completed_orders: int
    in_progress_orders: int
    total_quantity: int
    defect_rate: float
    
    class Config:
        from_attributes = True
