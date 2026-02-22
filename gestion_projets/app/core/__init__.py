"""
Configuration du module gestion de projets

Ce module contient les configurations et utilitaires
pour le module de gestion de projets.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from typing import List, Dict
from datetime import datetime, timedelta


class ProjectManager:
    """Gestionnaire de projets"""
    
    @staticmethod
    def calculate_progress(tasks: List[dict]) -> int:
        """
        Calcule la progression globale du projet.
        
        Args:
            tasks: Tâches
        
        Returns:
            Pourcentage de progression
        """
        if not tasks:
            return 0
        
        total_progress = sum(task.get("progress", 0) for task in tasks)
        
        return total_progress // len(tasks)
    
    @staticmethod
    def check_milestone(milestone: dict, tasks: List[dict]) -> dict:
        """
        Vérifie si un jalon est atteint.
        
        Args:
            milestone: Jalon
            tasks: Tâches liées
        
        Returns:
            Statut du jalon
        """
        completed_tasks = sum(
            1 for t in tasks 
            if t.get("status") == "terminee"
        )
        
        total_tasks = len(tasks)
        
        return {
            "completed": completed_tasks,
            "total": total_tasks,
            "percent": (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0,
            "achieved": completed_tasks == total_tasks and total_tasks > 0
        }


class TaskManager:
    """Gestionnaire de tâches"""
    
    @staticmethod
    def calculate_urgency(task: dict) -> str:
        """
        Calcule l'urgence d'une tâche.
        
        Args:
            task: Tâche
        
        Returns:
            Niveau d'urgence
        """
        due_date = task.get("due_date")
        
        if not due_date:
            return "normale"
        
        days_until_due = (due_date - datetime.now()).days
        
        if days_until_due < 0:
            return "critique"
        elif days_until_due <= 2:
            return "haute"
        elif days_until_due <= 7:
            return "moyenne"
        else:
            return "basse"
    
    @staticmethod
    def assign_priority(task: dict) -> str:
        """
        Assigne la priorité selon les critères.
        
        Args:
            task: Tâche
        
        Returns:
            Priorité
        """
        # Priorité selon le type
        priority = task.get("priority", "normale")
        
        # Ajuster selon l'urgence
        urgency = TaskManager.calculate_urgency(task)
        
        if urgency == "critique":
            priority = "urgente"
        
        return priority


class ResourceAllocation:
    """Allocation des ressources"""
    
    @staticmethod
    def check_team_availability(
        team_members: List[dict],
        start_date: datetime,
        end_date: datetime
    ) -> dict:
        """
        Vérifie la disponibilité de l'équipe.
        
        Args:
            team_members: Membres de l'équipe
            start_date: Date de début
            end_date: Date de fin
        
        Returns:
            Disponibilité
        """
        conflicts = []
        available = []
        
        for member in team_members:
            member_start = member.get("start_date")
            member_end = member.get("end_date")
            
            # Vérifier le chevauchement
            if member_start and member_end:
                if (start_date <= member_end and end_date >= member_start):
                    conflicts.append({
                        "member_id": member.get("user_id"),
                        "conflict_period": (member_start, member_end)
                    })
                else:
                    available.append(member.get("user_id"))
            else:
                available.append(member.get("user_id"))
        
        return {
            "available": available,
            "conflicts": conflicts,
            "all_available": len(conflicts) == 0
        }


class BudgetTracker:
    """Suivi du budget"""
    
    @staticmethod
    def calculate_budget_status(
        planned: float,
        actual: float,
        committed: float
    ) -> dict:
        """
        Calcule le statut du budget.
        
        Args:
            planned: Budgété
            actual: Dépensé
            committed: Engagé
        
        Returns:
            Statut
        """
        remaining = planned - actual
        
        variance = ((actual - planned) / planned * 100) if planned > 0 else 0
        
        return {
            "planned": planned,
            "actual": actual,
            "committed": committed,
            "remaining": remaining,
            "variance_percent": variance,
            "over_budget": actual > planned,
            "at_risk": remaining < (planned * 0.1)  # Moins de 10% restant
        }


class RiskAssessment:
    """Évaluation des risques"""
    
    @staticmethod
    def assess_project_risks(
        project: dict,
        tasks: List[dict],
        budget_status: dict
    ) -> List[dict]:
        """
        Évalue les risques du projet.
        
        Args:
            project: Projet
            tasks: Tâches
            budget_status: Statut du budget
        
        Returns:
            Liste des risques
        """
        risks = []
        
        # Risque de délai
        overdue_tasks = [
            t for t in tasks 
            if t.get("status") != "terminee" and 
            t.get("due_date") and 
            t.get("due_date") < datetime.now()
        ]
        
        if overdue_tasks:
            risks.append({
                "type": "delai",
                "severity": "haute",
                "description": f"{len(overdue_tasks)} tâche(s) en retard"
            })
        
        # Risque budget
        if budget_status.get("over_budget"):
            risks.append({
                "type": "budget",
                "severity": "critique",
                "description": "Budget dépassé"
            })
        
        # Risque de ressources
        incomplete_tasks = [t for t in tasks if not t.get("assigned_to")]
        
        if incomplete_tasks:
            risks.append({
                "type": "ressource",
                "severity": "moyenne",
                "description": f"{len(incomplete_tasks)} tâche(s) non assignée(s)"
            })
        
        return risks


def generate_project_report(
    project: dict,
    tasks: List[dict],
    milestones: List[dict],
    budget: dict
) -> dict:
    """
    Génère un rapport de projet.
    
    Args:
        project: Projet
        tasks: Tâches
        milestones: Jalons
        budget: Budget
    
    Returns:
        Rapport
    """
    progress = ProjectManager.calculate_progress(tasks)
    budget_status = BudgetTracker.calculate_budget_status(
        budget.get("planned", 0),
        budget.get("actual", 0),
        budget.get("committed", 0)
    )
    risks = RiskAssessment.assess_project_risks(project, tasks, budget_status)
    
    return {
        "project": project,
        "progress_percent": progress,
        "total_tasks": len(tasks),
        "completed_tasks": sum(1 for t in tasks if t.get("status") == "terminee"),
        "total_milestones": len(milestones),
        "completed_milestones": sum(1 for m in milestones if m.get("is_completed")),
        "budget": budget_status,
        "risks": risks,
        "generated_at": datetime.now()
    }
