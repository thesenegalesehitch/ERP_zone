"""
Configuration du module production

Ce module contient les configurations et utilitaires
pour le module de gestion de la production.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from typing import List, Dict
from datetime import datetime, timedelta


class ProductionPlanner:
    """Planificateur de production"""
    
    @staticmethod
    def create_production_order(
        product_id: int,
        quantity: int,
        priority: str = "normale",
        due_date: datetime = None
    ) -> Dict:
        """
        Crée un ordre de production.
        
        Args:
            product_id: ID produit
            quantity: Quantité
            priority: Priorité
            due_date: Date d'échéance
        
        Returns:
            Ordre de production
        """
        return {
            "product_id": product_id,
            "quantity": quantity,
            "priority": priority,
            "due_date": due_date,
            "status": "planifie",
            "created_at": datetime.now()
        }
    
    @staticmethod
    def calculate_production_time(
        quantity: int,
        hourly_capacity: float,
        efficiency: float = 0.85
    ) -> float:
        """
        Calcule le temps de production.
        
        Args:
            quantity: Quantité
            hourly_capacity: Capacité horaire
            efficiency: Efficacité
        
        Returns:
            Heures nécessaires
        """
        return quantity / (hourly_capacity * efficiency)


class ManufacturingProcess:
    """Processus de fabrication"""
    
    @staticmethod
    def calculate_bom_cost(
        bill_of_materials: List[Dict]
    ) -> float:
        """
        Calcule le coût de la nomenclature.
        
        Args:
            bill_of_materials: Nomenclature
        
        Returns:
            Coût total
        """
        total = 0
        
        for item in bill_of_materials:
            quantity = item.get("quantity", 0)
            unit_cost = item.get("unit_cost", 0)
            total += quantity * unit_cost
        
        return total
    
    @staticmethod
    def check_material_availability(
        required_materials: List[Dict],
        available_stock: Dict
    ) -> Dict:
        """
        Vérifie la disponibilité des matériaux.
        
        Args:
            required_materials: Matériaux requis
            available_stock: Stock disponible
        
        Returns:
            Disponibilité
        """
        available = []
        unavailable = []
        
        for material in required_materials:
            material_id = material.get("material_id")
            required_qty = material.get("quantity", 0)
            available_qty = available_stock.get(material_id, 0)
            
            if available_qty >= required_qty:
                available.append({
                    "material_id": material_id,
                    "required": required_qty,
                    "available": available_qty,
                    "sufficient": True
                })
            else:
                unavailable.append({
                    "material_id": material_id,
                    "required": required_qty,
                    "available": available_qty,
                    "shortage": required_qty - available_qty
                })
        
        return {
            "all_available": len(unavailable) == 0,
            "available": available,
            "unavailable": unavailable
        }


class QualityControl:
    """Contrôle qualité"""
    
    @staticmethod
    def calculate_defect_rate(
        total_items: int,
        defective_items: int
    ) -> Dict:
        """
        Calcule le taux de défaut.
        
        Args:
            total_items: Total des articles
            defective_items: Articles défectueux
        
        Returns:
            Taux
        """
        if total_items == 0:
            return {"defect_rate": 0, "quality_rate": 100}
        
        defect_rate = (defective_items / total_items) * 100
        quality_rate = 100 - defect_rate
        
        return {
            "defect_rate": defect_rate,
            "quality_rate": quality_rate,
            "total_items": total_items,
            "defective_items": defective_items,
            "accepted_items": total_items - defective_items
        }
    
    @staticmethod
    def perform_quality_check(
        batch_id: int,
        specifications: Dict,
        measurements: Dict
    ) -> Dict:
        """
        Effectue un contrôle qualité.
        
        Args:
            batch_id: ID lot
            specifications: Spécifications
            measurements: Mesures
        
        Returns:
            Résultat
        """
        passed_checks = []
        failed_checks = []
        
        for spec_name, spec_value in specifications.items():
            measured_value = measurements.get(spec_name)
            
            if measured_value is None:
                failed_checks.append({
                    "check": spec_name,
                    "reason": "missing_measurement"
                })
                continue
            
            tolerance = spec_value.get("tolerance", 0)
            target = spec_value.get("target")
            
            if abs(measured_value - target) <= tolerance:
                passed_checks.append({
                    "check": spec_name,
                    "measured": measured_value,
                    "target": target,
                    "status": "passed"
                })
            else:
                failed_checks.append({
                    "check": spec_name,
                    "measured": measured_value,
                    "target": target,
                    "status": "failed"
                })
        
        return {
            "batch_id": batch_id,
            "passed": len(passed_checks),
            "failed": len(failed_checks),
            "all_passed": len(failed_checks) == 0,
            "details": {
                "passed": passed_checks,
                "failed": failed_checks
            }
        }


class WorkStationManager:
    """Gestionnaire d_POSTES de travail"""
    
    @staticmethod
    def calculate_utilization(
        actual_output: float,
        capacity: float
    ) -> float:
        """
        Calcule le taux d'utilisation.
        
        Args:
            actual_output: Production réelle
            capacity: Capacité
        
        Returns:
            Taux
        """
        if capacity == 0:
            return 0
        
        return (actual_output / capacity) * 100
    
    @staticmethod
    def check_maintenance_due(
        last_maintenance: datetime,
        operating_hours: int,
        maintenance_interval: int = 1000
    ) -> Dict:
        """
        Vérifie si maintenance nécessaire.
        
        Args:
            last_maintenance: Dernière maintenance
            operating_hours: Heures de fonctionnement
            interval: Intervalle de maintenance
        
        Returns:
            Statut
        """
        hours_since_maintenance = operating_hours
        hours_until_due = maintenance_interval - hours_since_maintenance
        
        return {
            "maintenance_due": hours_since_maintenance >= maintenance_interval,
            "hours_since_maintenance": hours_since_maintenance,
            "hours_until_due": hours_until_due,
            "urgency": "critique" if hours_until_due < 0 else \
                      "haute" if hours_until_due < 100 else \
                      "moyenne" if hours_until_due < 250 else "basse"
        }


class CostCalculator:
    """Calculateur de coûts"""
    
    @staticmethod
    def calculate_production_cost(
        materials_cost: float,
        labor_hours: float,
        labor_rate: float,
        overhead_rate: float = 0.2
    ) -> Dict:
        """
        Calcule le coût de production.
        
        Args:
            materials_cost: Coût matériaux
            labor_hours: Heures de travail
            labor_rate: Taux horaire
            overhead_rate: Taux des frais généraux
        
        Returns:
            Coût
        """
        labor_cost = labor_hours * labor_rate
        overhead = (materials_cost + labor_cost) * overhead_rate
        total_cost = materials_cost + labor_cost + overhead
        
        return {
            "materials": materials_cost,
            "labor": labor_cost,
            "overhead": overhead,
            "total": total_cost,
            "unit_cost": total_cost  # Par unité si quantité = 1
        }


class SchedulingOptimizer:
    """Optimiseur d'ordonnancement"""
    
    @staticmethod
    def schedule_production(
        orders: List[Dict],
        workstations: List[Dict]
    ) -> List[Dict]:
        """
        Planifie la production.
        
        Args:
            orders: Ordres de production
            workstations: Postes de travail
        
        Returns:
            Planning
        """
        schedule = []
        
        for order in orders:
            # Trouver le poste disponible
            for workstation in workstations:
                if workstation.get("available"):
                    schedule.append({
                        "order_id": order.get("id"),
                        "workstation_id": workstation.get("id"),
                        "start_time": datetime.now(),
                        "estimated_end": datetime.now() + timedelta(
                            hours=order.get("estimated_hours", 8)
                        )
                    })
                    break
        
        return schedule


def generate_production_report(
    production_orders: List[Dict],
    quality_checks: List[Dict],
    workstations: List[Dict]
) -> Dict:
    """
    Génère un rapport de production.
    
    Args:
        orders: Ordres de production
        quality_checks: Contrôles qualité
        workstations: Postes
    
    Returns:
        Rapport
    """
    completed = sum(1 for o in production_orders if o.get("status") == "termine")
    in_progress = sum(1 for o in production_orders if o.get("status") == "en_cours")
    
    total_defects = sum(q.get("defective_items", 0) for q in quality_checks)
    total_items = sum(q.get("total_items", 0) for q in quality_checks)
    
    return {
        "orders": {
            "total": len(production_orders),
            "completed": completed,
            "in_progress": in_progress
        },
        "quality": {
            "total_items": total_items,
            "defects": total_defects,
            "defect_rate": (total_defects / total_items * 100) if total_items > 0 else 0
        },
        "workstations_count": len(workstations),
        "generated_at": datetime.now()
    }
