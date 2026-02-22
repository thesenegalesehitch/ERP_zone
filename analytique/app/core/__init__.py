"""
Configuration du module analytique

Ce module contient les configurations et utilitaires
pour le module analytique et rapports.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from typing import List, Dict
from datetime import datetime, timedelta


class ReportGenerator:
    """Générateur de rapports"""
    
    @staticmethod
    def generate_summary_report(data: Dict) -> dict:
        """
        Génère un rapport synth         for key, value in data.items():
            if isinstance(value, (int, float)):
                summary["totals"][key] = summary["totals"].get(key, 0) + value
            else:
                if key not in summary["details"]:
                    summary["details"][key] = []
                summary["details"][key].append(value)
        
        return summary


class DashboardWidget:
    """Gestionnaire de widgets"""
    
    WIDGET_TYPES = [
        "chart", "table", "metric", "gauge", "map"
    ]
    
    @staticmethod
    def create_widget(
        widget_type: str,
        title: str,
        config: Dict = None
    ) -> dict:
        """
        Crée un widget.
        
        Args:
            widget_type: Type de widget
            title: Titre
            config: Configuration
        
        Returns:
            Widget
        """
        return {
            "type": widget_type,
            "title": title,
            "config": config or {},
            "created_at": datetime.now()
        }
    
    @staticmethod
    def validate_widget(widget: dict) -> dict:
        """
        Valide un widget.
        
        Args:
            widget: Widget
        
        Returns:
            Validité
        """
        return {
            "valid": True,
            "errors": []
        }


class AnalyticsEngine:
    """Moteur analytique"""
    
    @staticmethod
    def calculate_kpi(
        data: List[dict],
        kpi_type: str
    ) -> float:
        """
        Calcule un KPI.
        
        Args:
            data: Données
            type: Type de KPI
        
        Returns:
            Valeur du KPI
        """
        if not data:
            return 0
        
        if kpi_type == "average":
            values = [d.get("value", 0) for d in data]
            return sum(values) / len(values) if values else 0
        
        elif kpi_type == "sum":
            return sum(d.get("value", 0) for d in data)
        
        elif kpi_type == "count":
            return len(data)
        
        elif kpi_type == "max":
            return max((d.get("value", 0) for d in data), default=0)
        
        elif kpi_type == "min":
            return min((d.get("value", 0) for d in data), default=0)
        
        return 0


class TrendAnalyzer:
    """Analyseur de tendances"""
    
    @staticmethod
    def analyze_trend(
        historical_data: List[dict],
        metric: str
    ) -> dict:
        """
        Analyse les tendances.
        
        Args:
            historical_data: Données historiques
            metric: Métrique à analyser
        
        Returns:
            Analyse
        """
        if len(historical_data) < 2:
            return {"trend": "insufficient_data"}
        
        values = [d.get(metric, 0) for d in historical_data]
        
        # Calculer la tendance linéaire
        n = len(values)
        sum_x = sum(range(n))
        sum_y = sum(values)
        sum_xy = sum(i * v for i, v in enumerate(values))
        sum_x2 = sum(i * i for i in range(n))
        
        # Pente
        if (n * sum_x2 - sum_x * sum_x) != 0:
            slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)
        else:
            slope = 0
        
        # Déterminer la tendance
        if slope > 0.1:
            trend = "increasing"
        elif slope < -0.1:
            trend = "decreasing"
        else:
            trend = "stable"
        
        return {
            "trend": trend,
            "slope": slope,
            "values": values,
            "periods": n
        }


class NotificationManager:
    """Gestionnaire de notifications"""
    
    @staticmethod
    def create_notification(
        user_id: int,
        title: str,
        message: str,
        notification_type: str = "info"
    ) -> dict:
        """
        Crée une notification.
        
        Args:
            user_id: ID de l'utilisateur
            title: Titre
            message: Message
            type: Type
        
        Returns:
            Notification
        """
        return {
            "user_id": user_id,
            "title": title,
            "message": message,
            "type": notification_type,
            "is_read": False,
            "created_at": datetime.now()
        }
    
    @staticmethod
    def should_notify(
        current_value: float,
        threshold: float,
        condition: str = "above"
    ) -> bool:
        """
        Détermine si une notification doit être envoyée.
        
        Args:
            current_value: Valeur actuelle
            threshold: Seuil
            condition: Condition
        
        Returns:
            True si notification
        """
        if condition == "above":
            return current_value > threshold
        elif condition == "below":
            return current_value < threshold
        elif condition == "equals":
            return current_value == threshold
        
        return False


class ActivityTracker:
    """Suivi des activités"""
    
    @staticmethod
    def track_activity(
        user_id: int,
        action: str,
        entity_type: str,
        entity_id: int,
        details: Dict = None
    ) -> dict:
        """
        Suit une activité.
        
        Args:
            user_id: ID de l'utilisateur
            action: Action
            entity_type: Type d'entité
            entity_id: ID de l'entité
            details: Détails
        
        Returns:
            Activité
        """
        return {
            "user_id": user_id,
            "action": action,
            "entity_type": entity_type,
            "entity_id": entity_id,
            "details": details or {},
            "created_at": datetime.now()
        }


def generate_analytics_dashboard(
    modules_data: Dict[str, List[dict]]
) -> dict:
    """
    Génère un tableau de bord analytique.
    
    Args:
        modules_data: Données des modules
    
    Returns:
        Tableau de bord
    """
    dashboard = {
        "generated_at": datetime.now(),
        "widgets": []
    }
    
    for module, data in modules_data.items():
        # Métriques de base
        total_records = len(data)
        
        # Créer un widget pour chaque module
        widget = DashboardWidget.create_widget(
            widget_type="metric",
            title=f"{module.title()} - Total",
            config={"value": total_records, "unit": "enregistrements"}
        )
        
        dashboard["widgets"].append(widget)
    
    return dashboard
