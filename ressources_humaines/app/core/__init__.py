"""
Configuration du module ressources humaines

Ce module contient les configurations et utilitaires
pour le module de gestion des ressources humaines.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from typing import List, Dict
from datetime import datetime, timedelta


class EmployeeManager:
    """Gestionnaire d'employés"""
    
    @staticmethod
    def calculate_years_of_service(
        hire_date: datetime,
        end_date: datetime = None
    ) -> float:
        """
        Calcule les années d'ancienneté.
        
        Args:
            hire_date: Date d'embauche
            end_date: Date de fin (optionnel)
        
        Returns:
            Années d'ancienneté
        """
        current_date = end_date if end_date else datetime.now()
        delta = current_date - hire_date
        return delta.days / 365.25
    
    @staticmethod
    def calculate_termination_severance(
        salary: float,
        years_of_service: float
    ) -> float:
        """
        Calcule l'indemnité de licenciement.
        
        Args:
            salary: Salaire
            years_of_service: Années d'ancienneté
        
        Returns:
            Indemnité
        """
        # Calcul selon la législation du Sénégal
        if years_of_service < 1:
            return 0
        elif years_of_service < 5:
            return salary * years_of_service * 0.5
        else:
            return salary * years_of_service * 0.7


class PayrollCalculator:
    """Calculateur de paie"""
    
    @staticmethod
    def calculate_gross_to_net(
        gross_salary: float,
        employee_id: int = None
    ) -> Dict:
        """
        Calcule le salaire net à partir du brut.
        
        Args:
            gross_salary: Salaire brut
            employee_id: ID employé
        
        Returns:
            Détails du salaire
        """
        # Cotisations sociales (exemple pour le Sénégal)
        cnsst = gross_salary * 0.024  # Caisse Nationale de Prévoyance Sociale
        ipm = gross_salary * 0.03       # Institution de Prévoyance Maladie
        unemployment = gross_salary * 0.02
        
        total_deductions = cnsst + ipm + unemployment
        
        # Impôt sur le revenu
        taxable_base = gross_salary - total_deductions
        income_tax = 0
        
        if taxable_base > 600000:  # Seuil
            income_tax = (taxable_base - 600000) * 0.30
        elif taxable_base > 300000:
            income_tax = (taxable_base - 300000) * 0.20
        elif taxable_base > 150000:
            income_tax = (taxable_base - 150000) * 0.10
        
        net_salary = gross_salary - total_deductions - income_tax
        
        return {
            "gross_salary": gross_salary,
            "cnsst": cnsst,
            "ipm": ipm,
            "unemployment": unemployment,
            "income_tax": income_tax,
            "total_deductions": total_deductions + income_tax,
            "net_salary": net_salary
        }
    
    @staticmethod
    def calculate_overtime(
        hours: float,
        hourly_rate: float,
        multiplier: float = 1.5
    ) -> float:
        """
        Calcule les heures supplémentaires.
        
        Args:
            hours: Heures
            hourly_rate: Taux horaire
            multiplier: Multiplicateur
        
        Returns:
            Montant
        """
        return hours * hourly_rate * multiplier


class LeaveManager:
    """Gestionnaire de congés"""
    
    @staticmethod
    def calculate_annual_leave_entitlement(
        years_of_service: float
    ) -> int:
        """
        Calcule les droits aux congés annuels.
        
        Args:
            years_of_service: Années d'ancienneté
        
        Returns:
            Jours de congés
        """
        base_days = 18
        
        if years_of_service >= 20:
            return base_days + 12
        elif years_of_service >= 10:
            return base_days + 6
        elif years_of_service >= 5:
            return base_days + 3
        else:
            return base_days
    
    @staticmethod
    def check_leave_balance(
        taken_days: int,
        entitled_days: int
    ) -> Dict:
        """
        Vérifie le solde de congés.
        
        Args:
            taken_days: Jours pris
            entitled_days: Jours dus
        
        Returns:
            Solde
        """
        remaining = entitled_days - taken_days
        
        return {
            "taken": taken_days,
            "entitled": entitled_days,
            "remaining": remaining,
            "can_take_more": remaining > 0
        }
    
    @staticmethod
    def calculate_maternity_leave(
        start_date: datetime,
        has_medical_complication: bool = False
    ) -> Dict:
        """
        Calcule le congé de maternité.
        
        Args:
            start_date: Date de début
            complication: Complications médicales
        
        Returns:
            Détails
        """
        # Selon le Code du Travail Sénégalais
        base_duration = 98  # 14 semaines
        
        if has_medical_complication:
            base_duration += 14
        
        end_date = start_date + timedelta(days=base_duration)
        
        return {
            "start_date": start_date,
            "end_date": end_date,
            "duration_days": base_duration,
            "paid": True
        }


class PerformanceEvaluator:
    """Évaluateur de performance"""
    
    @staticmethod
    def calculate_performance_score(
        objectives: List[Dict],
        competencies: List[Dict]
    ) -> Dict:
        """
        Calcule le score de performance.
        
        Args:
            objectives: Objectifs
            competencies: Compétences
        
        Returns:
            Score
        """
        # Pondération: 60% objectifs, 40% compétences
        objective_score = sum(o.get("score", 0) * o.get("weight", 1) 
                              for o in objectives)
        objective_weight = sum(o.get("weight", 1) for o in objectives)
        
        competency_score = sum(c.get("score", 0) * c.get("weight", 1) 
                              for c in competencies)
        competency_weight = sum(c.get("weight", 1) for c in competencies)
        
        final_score = (
            (objective_score / objective_weight * 0.6) if objective_weight > 0 else 0
        ) + (
            (competency_score / competency_weight * 0.4) if competency_weight > 0 else 0
        )
        
        return {
            "score": final_score,
            "objective_score": objective_score / objective_weight if objective_weight > 0 else 0,
            "competency_score": competency_score / competency_weight if competency_weight > 0 else 0,
            "rating": "excellent" if final_score >= 4.5 else \
                     "bien" if final_score >= 3.5 else \
                     "satisfaisant" if final_score >= 2.5 else \
                     "insatisfaisant"
        }


class AttendanceTracker:
    """Suivi de présence"""
    
    @staticmethod
    def calculate_work_hours(
        check_in: datetime,
        check_out: datetime,
        breaks_minutes: int = 60
    ) -> float:
        """
        Calcule les heures de travail.
        
        Args:
            check_in: Arrivée
            check_out: Départ
            breaks_minutes: Minutes de pause
        
        Returns:
            Heures travaillées
        """
        if not check_in or not check_out:
            return 0
        
        delta = check_out - check_in
        total_minutes = delta.total_seconds() / 60
        work_minutes = total_minutes - breaks_minutes
        
        return work_minutes / 60
    
    @staticmethod
    def get_attendance_summary(
        records: List[Dict],
        period_start: datetime,
        period_end: datetime
    ) -> Dict:
        """
        Génère un résumé de présence.
        
        Args:
            records: Enregistrements
            period_start: Début de période
            period_end: Fin de période
        
        Returns:
            Résumé
        """
        total_days = (period_end - period_start).days + 1
        present_days = sum(1 for r in records if r.get("status") == "present")
        absent_days = sum(1 for r in records if r.get("status") == "absent")
        late_days = sum(1 for r in records if r.get("status") == "late")
        
        return {
            "total_days": total_days,
            "present": present_days,
            "absent": absent_days,
            "late": late_days,
            "attendance_rate": (present_days / total_days * 100) if total_days > 0 else 0
        }


class ContractManager:
    """Gestionnaire de contrats"""
    
    @staticmethod
    def check_contract_renewal(
        end_date: datetime,
        notice_days: int = 30
    ) -> Dict:
        """
        Vérifie le renouvellement de contrat.
        
        Args:
            end_date: Date de fin
            notice_days: Jours de préavis
        
        Returns:
            Statut
        """
        days_until_end = (end_date - datetime.now()).days
        needs_renewal = days_until_end <= notice_days
        
        return {
            "days_until_end": days_until_end,
            "needs_renewal": needs_renewal,
            "action": "renouveler" if needs_renewal else "aucune"
        }


def generate_employee_dossier(
    employee: Dict,
    contracts: List[Dict],
    leaves: List[Dict],
    evaluations: List[Dict]
) -> Dict:
    """
    Génère le dossier employé.
    
    Args:
        employee: Employé
        contracts: Contrats
        leaves: Congés
        evaluations: Évaluations
    
    Returns:
        Dossier
    """
    years_of_service = EmployeeManager.calculate_years_of_service(
        employee.get("hire_date")
    )
    leave_balance = LeaveManager.check_leave_balance(
        leaves.get("taken", 0),
        LeaveManager.calculate_annual_leave_entitlement(years_of_service)
    )
    
    return {
        "employee": employee,
        "years_of_service": years_of_service,
        "leave_balance": leave_balance,
        "contracts_count": len(contracts),
        "evaluations_count": len(evaluations),
        "generated_at": datetime.now()
    }
