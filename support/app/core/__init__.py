"""
Configuration du module support

Ce module contient les configurations et utilitaires
pour le module de support client.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from typing import List, Dict
from datetime import datetime, timedelta


class TicketManager:
    """Gestionnaire de tickets"""
    
    @staticmethod
    def create_ticket(
        subject: str,
        description: str,
        customer_id: int,
        priority: str = "moyenne",
        category: str = "autre"
    ) -> Dict:
        """
        Crée un ticket de support.
        
        Args:
            subject: Sujet
            description: Description
            customer_id: ID client
            priority: Priorité
            category: Catégorie
        
        Returns:
            Ticket
        """
        return {
            "subject": subject,
            "description": description,
            "customer_id": customer_id,
            "priority": priority,
            "category": category,
            "status": "ouvert",
            "created_at": datetime.now(),
            "assigned_to": None,
            "resolved_at": None
        }
    
    @staticmethod
    def calculate_sla_deadline(
        priority: str,
        business_hours_only: bool = True
    ) -> datetime:
        """
        Calcule l'échéance SLA.
        
        Args:
            priority: Priorité
            business_hours_only: Heures ouvrables seulement
        
        Returns:
            Échéance
        """
        sla_hours = {
            "critique": 4,
            "haute": 24,
            "moyenne": 72,
            "basse": 168
        }
        
        hours = sla_hours.get(priority, 72)
        
        if business_hours_only:
            # Ajouter les jours ouvrables
            deadline = datetime.now()
            remaining_hours = hours
            
            while remaining_hours > 0:
                deadline += timedelta(hours=1)
                # Skip weekends
                if deadline.weekday() < 5 and 8 <= deadline.hour < 18:
                    remaining_hours -= 1
            
            return deadline
        else:
            return datetime.now() + timedelta(hours=hours)
    
    @staticmethod
    def check_escalation_needed(
        ticket: Dict,
        escalation_thresholds: Dict = None
    ) -> Dict:
        """
        Vérifie si escalade nécessaire.
        
        Args:
            ticket: Ticket
            thresholds: Seuils d'escalade
        
        Returns:
            Statut
        """
        if escalation_thresholds is None:
            escalation_thresholds = {
                "response_time": 24,  # heures
                "resolution_time": 72
            }
        
        age_hours = (datetime.now() - ticket.get("created_at")).total_seconds() / 3600
        
        needs_escalation = False
        reason = None
        
        if ticket.get("status") == "ouvert" and age_hours > escalation_thresholds["response_time"]:
            needs_escalation = True
            reason = "temps_reponse_depasse"
        
        if age_hours > escalation_thresholds["resolution_time"] and ticket.get("status") != "resolu":
            needs_escalation = True
            reason = "temps_resolution_depasse"
        
        return {
            "needs_escalation": needs_escalation,
            "reason": reason,
            "age_hours": age_hours
        }


class KnowledgeBase:
    """Base de connaissances"""
    
    @staticmethod
    def search_articles(
        query: str,
        articles: List[Dict]
    ) -> List[Dict]:
        """
        Recherche des articles.
        
        Args:
            query: Requête
            articles: Articles
        
        Returns:
            Résultats
        """
        results = []
        query_lower = query.lower()
        
        for article in articles:
            # Score de pertinence
            score = 0
            
            if query_lower in article.get("title", "").lower():
                score += 10
            
            if query_lower in article.get("content", "").lower():
                score += 5
            
            if query_lower in article.get("keywords", []):
                score += 7
            
            if score > 0:
                results.append({
                    **article,
                    "relevance_score": score
                })
        
        # Trier par pertinence
        results.sort(key=lambda x: x.get("relevance_score", 0), reverse=True)
        
        return results
    
    @staticmethod
    def get_article_helpfulness(
        article_id: int,
        votes: List[Dict]
    ) -> Dict:
        """
        Calcule l'utilité d'un article.
        
        Args:
            article_id: ID article
            votes: Votes
        
        Returns:
            Métriques
        """
        article_votes = [v for v in votes if v.get("article_id") == article_id]
        
        helpful = sum(1 for v in article_votes if v.get("helpful"))
        not_helpful = sum(1 for v in article_votes if not v.get("helpful"))
        total = len(article_votes)
        
        helpfulness_score = (helpful / total * 100) if total > 0 else 0
        
        return {
            "article_id": article_id,
            "helpful": helpful,
            "not_helpful": not_helpful,
            "total_votes": total,
            "helpfulness_score": helpfulness_score
        }


class ServiceLevelManager:
    """Gestionnaire de niveau de service"""
    
    @staticmethod
    def calculate_sla_compliance(
        tickets: List[Dict],
        sla_targets: Dict = None
    ) -> Dict:
        """
        Calcule la conformité SLA.
        
        Args:
            tickets: Tickets
            targets: Cibles SLA
        
        Returns:
            Conformité
        """
        if sla_targets is None:
            sla_targets = {
                "critique": {"response": 4, "resolution": 24},
                "haute": {"response": 24, "resolution": 72},
                "moyenne": {"response": 72, "resolution": 168},
                "basse": {"response": 168, "resolution": 336}
            }
        
        response_met = 0
        response_total = 0
        resolution_met = 0
        resolution_total = 0
        
        for ticket in tickets:
            priority = ticket.get("priority", "moyenne")
            targets = sla_targets.get(priority, {})
            
            # Vérifier temps de réponse
            first_response = ticket.get("first_response_at")
            if first_response:
                response_time = (first_response - ticket.get("created_at")).total_seconds() / 3600
                response_total += 1
                if response_time <= targets.get("response", 72):
                    response_met += 1
            
            # Vérifier temps de résolution
            if ticket.get("status") == "resolu":
                resolution_time = (
                    ticket.get("resolved_at") - ticket.get("created_at")
                ).total_seconds() / 3600
                resolution_total += 1
                if resolution_time <= targets.get("resolution", 168):
                    resolution_met += 1
        
        return {
            "response_compliance": (response_met / response_total * 100) if response_total > 0 else 100,
            "resolution_compliance": (resolution_met / resolution_total * 100) if resolution_total > 0 else 100,
            "tickets_analyzed": len(tickets),
            "response_met": response_met,
            "response_total": response_total,
            "resolution_met": resolution_met,
            "resolution_total": resolution_total
        }


class TeamPerformance:
    """Performance de l'équipe"""
    
    @staticmethod
    def calculate_agent_metrics(
        agent_id: int,
        tickets: List[Dict]
    ) -> Dict:
        """
        Calcule les métriques d'un agent.
        
        Args:
            agent_id: ID agent
            tickets: Tickets
        
        Returns:
            Métriques
        """
        agent_tickets = [t for t in tickets if t.get("assigned_to") == agent_id]
        
        resolved = [t for t in agent_tickets if t.get("status") == "resolu"]
        open_tickets = [t for t in agent_tickets if t.get("status") == "ouvert"]
        
        # Temps moyen de résolution
        if resolved:
            resolution_times = [
                (t.get("resolved_at") - t.get("created_at")).total_seconds() / 3600
                for t in resolved
                if t.get("resolved_at")
            ]
            avg_resolution_time = sum(resolution_times) / len(resolution_times) if resolution_times else 0
        else:
            avg_resolution_time = 0
        
        return {
            "agent_id": agent_id,
            "total_assigned": len(agent_tickets),
            "resolved": len(resolved),
            "open": len(open_tickets),
            "avg_resolution_time_hours": avg_resolution_time,
            "satisfaction_score": 0  # À calculer depuis les feedbacks
        }
    
    @staticmethod
    def get_workload_distribution(
        tickets: List[Dict],
        agents: List[Dict]
    ) -> Dict:
        """
        Calcule la distribution de charge.
        
        Args:
            tickets: Tickets
            agents: Agents
        
        Returns:
            Distribution
        """
        distribution = []
        
        for agent in agents:
            agent_tickets = [
                t for t in tickets 
                if t.get("assigned_to") == agent.get("id")
            ]
            
            distribution.append({
                "agent_id": agent.get("id"),
                "agent_name": agent.get("name"),
                "ticket_count": len(agent_tickets),
                "open_count": sum(1 for t in agent_tickets if t.get("status") == "ouvert")
            })
        
        # Trier par charge
        distribution.sort(key=lambda x: x.get("ticket_count", 0), reverse=True)
        
        avg_workload = sum(d.get("ticket_count", 0) for d in distribution) / len(agents) if agents else 0
        
        return {
            "distribution": distribution,
            "average_workload": avg_workload,
            "total_agents": len(agents)
        }


class AutoResponse:
    """Réponses automatiques"""
    
    @staticmethod
    def generate_auto_response(
        ticket: Dict,
        knowledge_base: List[Dict]
    ) -> str:
        """
        Génère une réponse automatique.
        
        Args:
            ticket: Ticket
            base: Base de connaissances
        
        Returns:
            Réponse
        """
        category = ticket.get("category")
        
        # Trouver un article pertinent
        articles = KnowledgeBase.search_articles(category, knowledge_base)
        
        if articles:
            return f"""
Merci de nous avoir contactés. 

Nous avons trouvé un article qui pourrait vous aider:

{articles[0].get('title')}

{articles[0].get('content', '')[:500]}...

Si cet article ne résout pas votre problème, notre équipe de support vous répondra sous peu.
"""
        
        return """
Merci de nous avoir contactés.

Votre ticket a été créé et notre équipe de support va le traiter dans les plus brefs délais.

Numéro de ticket: {ticket_id}
""".format(ticket_id=ticket.get("id"))


def generate_support_report(
    tickets: List[Dict],
    agents: List[Dict],
    knowledge_base: List[Dict]
) -> Dict:
    """
    Génère un rapport de support.
    
    Args:
        tickets: Tickets
        agents: Agents
        base: Base de connaissances
    
    Returns:
        Rapport
    """
    open_tickets = [t for t in tickets if t.get("status") == "ouvert"]
    resolved_tickets = [t for t in tickets if t.get("status") == "resolu"]
    
    sla = ServiceLevelManager.calculate_sla_compliance(tickets)
    workload = TeamPerformance.get_workload_distribution(tickets, agents)
    
    return {
        "summary": {
            "total_tickets": len(tickets),
            "open": len(open_tickets),
            "resolved": len(resolved_tickets),
            "resolution_rate": (len(resolved_tickets) / len(tickets) * 100) if tickets else 0
        },
        "sla_compliance": sla,
        "workload_distribution": workload,
        "articles_count": len(knowledge_base),
        "generated_at": datetime.now()
    }
