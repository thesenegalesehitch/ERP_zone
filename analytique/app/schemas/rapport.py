"""
Schémas de validation pour les rapports

Ce module définit les schémas Pydantic pour la validation
des données liées aux rapports analytiques.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class ReportBase(BaseModel):
    """Schéma de base pour un rapport"""
    name: str = Field(..., min_length=1, max_length=200)
    report_type: str


class ReportCreate(ReportBase):
    """Schéma pour créer un rapport"""
    parameters: Optional[Dict[str, Any]] = None


class ReportUpdate(BaseModel):
    """Schéma pour mettre à jour un rapport"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    parameters: Optional[Dict[str, Any]] = None


class ReportResponse(ReportBase):
    """Schéma pour la réponse d'un rapport"""
    id: int
    parameters: Optional[Dict[str, Any]] = None
    created_by: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class DashboardWidgetCreate(BaseModel):
    """Schéma pour créer un widget"""
    widget_type: str
    title: str
    data_source: str
    position_x: int = Field(default=0, ge=0)
    position_y: int = Field(default=0, ge=0)
    width: int = Field(default=1, ge=1, le=4)
    height: int = Field(default=1, ge=1, le=4)
    config: Optional[Dict[str, Any]] = None


class DashboardWidgetUpdate(BaseModel):
    """Schéma pour mettre à jour un widget"""
    title: Optional[str] = None
    position_x: Optional[int] = Field(None, ge=0)
    position_y: Optional[int] = Field(None, ge=0)
    width: Optional[int] = Field(None, ge=1, le=4)
    height: Optional[int] = Field(None, ge=1, le=4)
    config: Optional[Dict[str, Any]] = None


class DashboardWidgetResponse(BaseModel):
    """Schéma pour la réponse d'un widget"""
    id: int
    dashboard_id: int
    widget_type: str
    title: str
    data_source: str
    position_x: int
    position_y: int
    width: int
    height: int
    config: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class DashboardBase(BaseModel):
    """Schéma de base pour un tableau de bord"""
    name: str = Field(..., min_length=1, max_length=200)
    dashboard_type: str = Field(default="personnalise")


class DashboardCreate(DashboardBase):
    """Schéma pour créer un tableau de bord"""
    widgets: Optional[List[Dict[str, Any]]] = None


class DashboardUpdate(BaseModel):
    """Schéma pour mettre à jour un tableau de bord"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    widgets: Optional[List[Dict[str, Any]]] = None


class DashboardResponse(DashboardBase):
    """Schéma pour la réponse d'un tableau de bord"""
    id: int
    widgets: Optional[List[Dict[str, Any]]] = None
    created_by: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class KPIBase(BaseModel):
    """Schéma de base pour un KPI"""
    name: str = Field(..., min_length=1, max_length=200)
    kpi_type: str
    target_value: Optional[float] = None


class KPICreate(KPIBase):
    """Schéma pour créer un KPI"""
    data_source: str
    config: Optional[Dict[str, Any]] = None


class KPIUpdate(BaseModel):
    """Schéma pour mettre à jour un KPI"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    target_value: Optional[float] = None
    config: Optional[Dict[str, Any]] = None


class KPIResponse(KPIBase):
    """Schéma pour la réponse d'un KPI"""
    id: int
    data_source: str
    current_value: Optional[float] = None
    config: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ReportFilter(BaseModel):
    """Schéma pour filtrer les rapports"""
    report_type: Optional[str] = None
    created_by: Optional[int] = None


class DashboardFilter(BaseModel):
    """Schéma pour filtrer les tableaux de bord"""
    dashboard_type: Optional[str] = None
    created_by: Optional[int] = None
