"""
API Routes pour les rapports analytiques

Ce module définit les routes API pour les rapports et tableaux de bord.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from datetime import datetime


router = APIRouter(prefix="/rapports", tags=["analytique"])


# Mock data pour les tests
MOCK_REPORTS = [
    {
        "id": 1,
        "name": "Rapport des ventes mensuelles",
        "report_type": "vente",
        "parameters": {"month": 1, "year": 2026},
        "created_by": 1,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
]


@router.get("/")
async def get_reports(
    report_type: str = None,
    created_by: int = None
):
    """Récupère la liste des rapports"""
    reports = MOCK_REPORTS
    
    if report_type:
        reports = [r for r in reports if r["report_type"] == report_type]
    if created_by:
        reports = [r for r in reports if r["created_by"] == created_by]
    
    return {"reports": reports, "total": len(reports)}


@router.get("/{report_id}")
async def get_report(report_id: int):
    """Récupère un rapport par son ID"""
    for report in MOCK_REPORTS:
        if report["id"] == report_id:
            return report
    
    raise HTTPException(status_code=404, detail="Rapport non trouvé")


@router.post("/")
async def create_report(report_data: dict):
    """Crée un nouveau rapport"""
    new_report = {
        "id": len(MOCK_REPORTS) + 1,
        **report_data,
        "created_by": 1,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
    MOCK_REPORTS.append(new_report)
    return new_report


# Routes pour les tableaux de bord
MOCK_DASHBOARDS = []


@router.get("/tableaux-de-bord/")
async def get_dashboards(
    dashboard_type: str = None,
    created_by: int = None
):
    """Récupère la liste des tableaux de bord"""
    dashboards = MOCK_DASHBOARDS
    
    if dashboard_type:
        dashboards = [d for d in dashboards if d["dashboard_type"] == dashboard_type]
    if created_by:
        dashboards = [d for d in dashboards if d["created_by"] == created_by]
    
    return {"dashboards": dashboards, "total": len(dashboards)}


@router.post("/tableaux-de-bord/")
async def create_dashboard(dashboard_data: dict):
    """Crée un nouveau tableau de bord"""
    new_dashboard = {
        "id": len(MOCK_DASHBOARDS) + 1,
        **dashboard_data,
        "widgets": [],
        "created_by": 1,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
    MOCK_DASHBOARDS.append(new_dashboard)
    return new_dashboard


# Routes pour les KPI
MOCK_KPIS = []


@router.get("/kpi/")
async def get_kpis():
    """Récupère la liste des KPI"""
    return {"kpis": MOCK_KPIS, "total": len(MOCK_KPIS)}


@router.post("/kpi/")
async def create_kpi(kpi_data: dict):
    """Crée un nouveau KPI"""
    new_kpi = {
        "id": len(MOCK_KPIS) + 1,
        **kpi_data,
        "current_value": 0,
        "created_at": datetime.now()
    }
    MOCK_KPIS.append(new_kpi)
    return new_kpi


# Routes pour les statistiques globales
@router.get("/stats/ventes")
async def get_sales_stats(
    start_date: datetime = None,
    end_date: datetime = None
):
    """Récupère les statistiques de ventes"""
    return {
        "total_revenue": 0,
        "total_orders": 0,
        "average_order": 0,
        "top_products": []
    }


@router.get("/stats/stocks")
async def get_inventory_stats():
    """Récupère les statistiques de stock"""
    return {
        "total_products": 0,
        "low_stock_count": 0,
        "total_value": 0
    }


@router.get("/stats/rh")
async def get_hr_stats():
    """Récupère les statistiques RH"""
    return {
        "total_employees": 0,
        "active_employees": 0,
        "on_leave": 0
    }


@router.get("/export/{report_id}")
async def export_report(
    report_id: int,
    format: str = "pdf"
):
    """Exporte un rapport"""
    return {
        "report_id": report_id,
        "format": format,
        "url": f"/downloads/report_{report_id}.{format}"
    }
