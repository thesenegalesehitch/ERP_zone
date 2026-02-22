"""
Configuration du module gestion des clients

Ce module contient les configurations et utilitaires
pour le module de gestion de la (CRM).

Ce relation client fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from typing import List, Dict
from datetime import datetime, timedelta


class CustomerManager:
    """Gestionnaire de clients"""
    
    @staticmethod
    def calculate_customer_value(
        purchases: List[Dict],
        expected_future_purchases: int = 5
    ) -> Dict:
        """
        Calcule la valeur vie client (CLV).
        
        Args:
            purchases: Achats passés
            expected_future_purchases: Achats futurs attendus
        
        Returns:
            Valeur client
        """
        if not purchases:
            return {"clv": 0, "avg_purchase": 0, "purchase_count": 0}
        
        total_revenue = sum(p.get("amount", 0) for p in purchases)
        avg_purchase = total_revenue / len(purchases)
        clv = avg_purchase * expected_future_purchases
        
        return {
            "clv": clv,
            "avg_purchase": avg_purchase,
            "purchase_count": len(purchases),
            "total_revenue": total_revenue
        }
    
    @staticmethod
    def segment_customer(
        total_revenue: float,
        purchase_frequency: int,
        last_purchase_date: datetime
    ) -> str:
        """
        Segmente le client.
        
        Args:
            total_revenue: Revenu total
            purchase_frequency: Fréquence d'achat
            last_purchase_date: Dernier achat
        
        Returns:
            Segment
        """
        days_since_last = (datetime.now() - last_purchase_date).days
        
        # VIP: Revenue élevé, fréquence élevée, achat récent
        if total_revenue > 1000000 and purchase_frequency > 10 and days_since_last < 30:
            return "vip"
        
        # Fidèle: Achats réguliers
        if purchase_frequency > 5 and days_since_last < 90:
            return "fidele"
        
        # À risque: Pas d'achat depuis longtemps
        if days_since_last > 180:
            return "a_risque"
        
        # Nouveau
        if days_since_last < 30:
            return "nouveau"
        
        # Inactif
        return "inactif"


class LeadManager:
    """Gestionnaire de prospects"""
    
    @staticmethod
    def calculate_lead_score(
        lead: Dict,
        criteria_weights: Dict = None
    ) -> Dict:
        """
        Calcule le score du prospect.
        
        Args:
            lead: Prospect
            weights: Pondérations
        
        Returns:
            Score
        """
        if criteria_weights is None:
            criteria_weights = {
                "budget": 0.3,
                "authority": 0.2,
                "need": 0.3,
                "timeline": 0.2
            }
        
        score = 0
        
        # Score budget
        budget_score = 0
        if lead.get("budget"):
            if lead["budget"] > 5000000:
                budget_score = 10
            elif lead["budget"] > 1000000:
                budget_score = 7
            elif lead["budget"] > 500000:
                budget_score = 5
            else:
                budget_score = 3
        
        # Score autorité
        authority_score = 0
        if lead.get("role") in ["dg", "directeur", "chef_service"]:
            authority_score = 10
        elif lead.get("role") in ["responsable", "manager"]:
            authority_score = 7
        else:
            authority_score = 3
        
        # Score besoin
        need_score = 0
        if lead.get("urgency") == "haute":
            need_score = 10
        elif lead.get("urgency") == "moyenne":
            need_score = 7
        else:
            need_score = 4
        
        # Score calendrier
        timeline_score = 0
        if lead.get("timeline") == "immediat":
            timeline_score = 10
        elif lead.get("timeline") == "court_terme":
            timeline_score = 7
        elif lead.get("timeline") == "moyen_terme":
            timeline_score = 5
        else:
            timeline_score = 2
        
        # Calcul pondéré
        score = (
            budget_score * criteria_weights["budget"] +
            authority_score * criteria_weights["authority"] +
            need_score * criteria_weights["need"] +
            timeline_score * criteria_weights["timeline"]
        )
        
        # Qualification
        if score >= 8:
            qualification = "hot"
        elif score >= 6:
            qualification = "warm"
        elif score >= 4:
            qualification = "cold"
        else:
            qualification = "nonqualifie"
        
        return {
            "score": score,
            "qualification": qualification,
            "breakdown": {
                "budget": budget_score,
                "authority": authority_score,
                "need": need_score,
                "timeline": timeline_score
            }
        }
    
    @staticmethod
    def get_conversion_probability(
        lead_score: float,
        industry_avg: float = 0.15
    ) -> float:
        """
        Calcule la probabilité de conversion.
        
        Args:
            lead_score: Score du prospect
            industry_avg: Moyenne du secteur
        
        Returns:
            Probabilité
        """
        # Normaliser le score (0-10) en probabilité
        base_prob = (lead_score / 10) * 0.5
        
        # Ajuster avec la moyenne du secteur
        adjusted_prob = (base_prob + industry_avg) / 2
        
        return min(adjusted_prob, 0.95)  # Max 95%


class CampaignManager:
    """Gestionnaire de campagnes"""
    
    @staticmethod
    def calculate_campaign_roi(
        campaign_costs: float,
        revenue_generated: float,
        leads_generated: int
    ) -> Dict:
        """
        Calcule le ROI de la campagne.
        
        Args:
            campaign_costs: Coûts
            revenue_generated: Revenu généré
            leads_generated: Prospects générés
        
        Returns:
            ROI
        """
        roi = ((revenue_generated - campaign_costs) / campaign_costs * 100) \
               if campaign_costs > 0 else 0
        
        cost_per_lead = campaign_costs / leads_generated if leads_generated > 0 else 0
        
        return {
            "roi_percent": roi,
            "revenue_generated": revenue_generated,
            "campaign_costs": campaign_costs,
            "leads_generated": leads_generated,
            "cost_per_lead": cost_per_lead,
            "profitable": revenue_generated > campaign_costs
        }
    
    @staticmethod
    def get_campaign_effectiveness(
        sent: int,
        opened: int,
        clicked: int,
        converted: int
    ) -> Dict:
        """
        Calcule l'efficacité de la campagne.
        
        Args:
            sent: Envoyés
            opened: Ouverts
            clicked: Cliqués
            converted: Convertis
        
        Returns:
            Métriques
        """
        open_rate = (opened / sent * 100) if sent > 0 else 0
        click_rate = (clicked / opened * 100) if opened > 0 else 0
        conversion_rate = (converted / clicked * 100) if clicked > 0 else 0
        
        return {
            "sent": sent,
            "opened": opened,
            "clicked": clicked,
            "converted": converted,
            "open_rate": open_rate,
            "click_rate": click_rate,
            "conversion_rate": conversion_rate
        }


class SupportTicketManager:
    """Gestionnaire de tickets de support"""
    
    @staticmethod
    def calculate_ticket_priority(
        ticket: Dict
    ) -> str:
        """
        Calcule la priorité du ticket.
        
        Args:
            ticket: Ticket
        
        Returns:
            Priorité
        """
        # Basé sur l'impact et l'urgence
        impact = ticket.get("impact", "moyen")
        urgency = ticket.get("urgency", "moyen")
        
        priority_matrix = {
            ("critique", "critique"): "critique",
            ("critique", "haute"): "critique",
            ("haute", "critique"): "critique",
            ("haute", "haute"): "haute",
            ("haute", "moyenne"): "haute",
            ("moyenne", "haute"): "haute",
            ("moyenne", "moyenne"): "moyenne",
            ("moyenne", "basse"): "basse",
            ("basse", "moyenne"): "basse",
            ("basse", "basse"): "basse",
        }
        
        return priority_matrix.get((impact, urgency), "moyenne")
    
    @staticmethod
    def calculate_sla_status(
        created_at: datetime,
        priority: str,
        resolution_time_hours: Dict = None
    ) -> Dict:
        """
        Calcule le statut SLA.
        
        Args:
            created_at: Date de création
            priority: Priorité
            resolution_time: Temps de résolution
        
        Returns:
            Statut
        """
        if resolution_time_hours is None:
            resolution_time_hours = {
                "critique": 4,
                "haute": 24,
                "moyenne": 72,
                "basse": 168
            }
        
        deadline = created_at + timedelta(
            hours=resolution_time_hours.get(priority, 72)
        )
        
        time_remaining = (deadline - datetime.now()).total_seconds() / 3600
        is_breached = time_remaining < 0
        
        return {
            "deadline": deadline,
            "hours_remaining": time_remaining,
            "is_breached": is_breached,
            "status": "breche" if is_breached else "ok"
        }


class SalesForecast:
    """Prévision des ventes"""
    
    @staticmethod
    def calculate_pipeline_value(
        opportunities: List[Dict],
        probability_threshold: float = 0.5
    ) -> Dict:
        """
        Calcule la valeur du pipeline.
        
        Args:
            opportunities: Opportunités
            threshold: Seuil de probabilité
        
        Returns:
            Valeur pipeline
        """
        weighted_value = 0
        total_value = 0
        
        for opp in opportunities:
            value = opp.get("value", 0)
            prob = opp.get("probability", 0) / 100
            
            total_value += value
            
            if prob >= probability_threshold:
                weighted_value += value * prob
        
        return {
            "total_value": total_value,
            "weighted_value": weighted_value,
            "opportunities_count": len(opportunities),
            "win_probability": (weighted_value / total_value * 100) if total_value > 0 else 0
        }


def generate_customer_report(
    customer: Dict,
    purchases: List[Dict],
    tickets: List[Dict]
) -> Dict:
    """
    Génère un rapport client.
    
    Args:
        customer: Client
        purchases: Achats
        tickets: Tickets
    
    Returns:
        Rapport
    """
    value = CustomerManager.calculate_customer_value(purchases)
    segment = CustomerManager.segment_customer(
        value["total_revenue"],
        value["purchase_count"],
        customer.get("last_purchase_date", datetime.now())
    )
    
    return {
        "customer": customer,
        "segment": segment,
        "customer_lifetime_value": value,
        "total_tickets": len(tickets),
        "open_tickets": sum(1 for t in tickets if t.get("status") == "ouvert"),
        "generated_at": datetime.now()
    }
