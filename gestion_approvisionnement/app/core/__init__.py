"""
Configuration du module gestion des approvisionnements

Ce module contient les configurations et utilitaires
pour le module de gestion des approvisionnements et achats.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from typing import List, Dict
from datetime import datetime, timedelta


class SupplierManager:
    """Gestionnaire de fournisseurs"""
    
    @staticmethod
    def evaluate_supplier(
        supplier: Dict,
        performance_data: List[Dict]
    ) -> Dict:
        """
        Évalue un fournisseur.
        
        Args:
            supplier: Fournisseur
            data: Données de performance
        
        Returns:
            Évaluation
        """
        if not performance_data:
            return {
                "score": 0,
                "rating": "non_evalue",
                "issues": []
            }
        
        # Calculer les métriques
        on_time_delivery = sum(1 for p in performance_data if p.get("on_time")) / len(performance_data) * 100
        quality_score = sum(p.get("quality_score", 0) for p in performance_data) / len(performance_data)
        
        # Score global
        score = (on_time_delivery * 0.4) + (quality_score * 0.6)
        
        # Déterminer la note
        if score >= 90:
            rating = "excellent"
        elif score >= 75:
            rating = "bien"
        elif score >= 60:
            rating = "moyen"
        else:
            rating = "faible"
        
        return {
            "score": score,
            "rating": rating,
            "on_time_delivery": on_time_delivery,
            "quality_score": quality_score,
            "orders_count": len(performance_data)
        }
    
    @staticmethod
    def compare_suppliers(
        suppliers: List[Dict],
        product_id: int
    ) -> List[Dict]:
        """
        Compare les fournisseurs pour un produit.
        
        Args:
            suppliers: Fournisseurs
            product_id: ID produit
        
        Returns:
            Comparaison
        """
        comparisons = []
        
        for supplier in suppliers:
            price = supplier.get("prices", {}).get(product_id, {}).get("price", 0)
            lead_time = supplier.get("prices", {}).get(product_id, {}).get("lead_time", 0)
            min_order = supplier.get("prices", {}).get(product_id, {}).get("min_order", 0)
            
            comparisons.append({
                "supplier_id": supplier.get("id"),
                "supplier_name": supplier.get("name"),
                "price": price,
                "lead_time": lead_time,
                "min_order": min_order
            })
        
        # Trier par prix
        comparisons.sort(key=lambda x: x.get("price", 0))
        
        return comparisons


class PurchaseOrderManager:
    """Gestionnaire de bons de commande"""
    
    @staticmethod
    def create_purchase_order(
        supplier_id: int,
        items: List[Dict],
        priority: str = "normale"
    ) -> Dict:
        """
        Crée un bon de commande.
        
        Args:
            supplier_id: ID fournisseur
            items: Articles
            priority: Priorité
        
        Returns:
            Bon de commande
        """
        subtotal = sum(item.get("quantity", 0) * item.get("unit_price", 0) for item in items)
        
        return {
            "supplier_id": supplier_id,
            "items": items,
            "priority": priority,
            "subtotal": subtotal,
            "tax": subtotal * 0.18,
            "total": subtotal * 1.18,
            "status": "en_attente",
            "created_at": datetime.now()
        }
    
    @staticmethod
    def approve_order(
        order: Dict,
        approver_id: int
    ) -> Dict:
        """
        Approuve une commande.
        
        Args:
            order: Commande
            approver_id: ID approbateur
        
        Returns:
            Commande approuvée
        """
        if order.get("status") != "en_attente":
            return {
                "success": False,
                "reason": "invalid_status"
            }
        
        order["status"] = "approuvee"
        order["approved_by"] = approver_id
        order["approved_at"] = datetime.now()
        
        return {
            "success": True,
            "order": order
        }
    
    @staticmethod
    def receive_order(
        order: Dict,
        received_items: List[Dict]
    ) -> Dict:
        """
        Réceptionne une commande.
        
        Args:
            order: Commande
            items: Articles reçus
        
        Returns:
            Réception
        """
        order["status"] = "recue"
        order["received_at"] = datetime.now()
        order["received_items"] = received_items
        
        # Vérifier la conformité
        ordered_items = order.get("items", [])
        discrepancies = []
        
        for ordered in ordered_items:
            received = next(
                (r for r in received_items if r.get("item_id") == ordered.get("item_id")),
                {}
            )
            
            ordered_qty = ordered.get("quantity", 0)
            received_qty = received.get("quantity", 0)
            
            if received_qty < ordered_qty:
                discrepancies.append({
                    "item_id": ordered.get("item_id"),
                    "ordered": ordered_qty,
                    "received": received_qty,
                    "shortage": ordered_qty - received_qty
                })
        
        order["discrepancies"] = discrepancies
        
        return {
            "success": True,
            "order": order,
            "has_discrepancies": len(discrepancies) > 0
        }


class RequisitionManager:
    """Gestionnaire de demandes d'achat"""
    
    @staticmethod
    def create_requisition(
        requester_id: int,
        items: List[Dict],
        justification: str
    ) -> Dict:
        """
        Crée une demande d'achat.
        
        Args:
            requester_id: ID demandeur
            items: Articles
            justification: Justification
        
        Returns:
            Demande
        """
        estimated_total = sum(
            item.get("quantity", 0) * item.get("estimated_price", 0)
            for item in items
        )
        
        return {
            "requester_id": requester_id,
            "items": items,
            "justification": justification,
            "estimated_total": estimated_total,
            "status": "soumise",
            "created_at": datetime.now()
        }
    
    @staticmethod
    def approve_requisition(
        requisition: Dict,
        approver_id: int,
        budget_available: float
    ) -> Dict:
        """
        Approuve une demande.
        
        Args:
            requisition: Demande
            approver_id: ID approbateur
            budget: Budget disponible
        
        Returns:
            Résultat
        """
        estimated_total = requisition.get("estimated_total", 0)
        
        if estimated_total > budget_available:
            return {
                "success": False,
                "reason": "insufficient_budget"
            }
        
        requisition["status"] = "approuvee"
        requisition["approved_by"] = approver_id
        requisition["approved_at"] = datetime.now()
        
        return {
            "success": True,
            "requisition": requisition
        }


class DeliveryScheduler:
    """Planificateur de livraisons"""
    
    @staticmethod
    def schedule_delivery(
        purchase_order_id: int,
        supplier: Dict,
        warehouse_location: str
    ) -> Dict:
        """
        Planifie une livraison.
        
        Args:
            order_id: ID commande
            supplier: Fournisseur
            warehouse: Emplacement entrepôt
        
        Returns:
            Livraison
        """
        lead_time = supplier.get("default_lead_time", 7)
        scheduled_date = datetime.now() + timedelta(days=lead_time)
        
        return {
            "purchase_order_id": purchase_order_id,
            "supplier_id": supplier.get("id"),
            "warehouse_location": warehouse_location,
            "scheduled_date": scheduled_date,
            "status": "planifiee",
            "created_at": datetime.now()
        }
    
    @staticmethod
    def track_delivery(
        delivery: Dict,
        current_location: str,
        eta: datetime
    ) -> Dict:
        """
        Suit la livraison.
        
        Args:
            delivery: Livraison
            location: Localisation actuelle
            eta: Arrivée prévue
        
        Returns:
            Suivi
        """
        delivery["current_location"] = current_location
        delivery["eta"] = eta
        delivery["last_update"] = datetime.now()
        
        return delivery


class CostAnalyzer:
    """Analyseur de coûts"""
    
    @staticmethod
    def analyze_purchase_costs(
        orders: List[Dict],
        period_months: int = 12
    ) -> Dict:
        """
        Analyse les coûts d'achat.
        
        Args:
            orders: Commandes
            period: Période en mois
        
        Returns:
            Analyse
        """
        now = datetime.now()
        period_start = now - timedelta(days=period_months * 30)
        
        period_orders = [
            o for o in orders
            if o.get("created_at", datetime.min) >= period_start
        ]
        
        total_spent = sum(o.get("total", 0) for o in period_orders)
        total_orders = len(period_orders)
        avg_order_value = total_spent / total_orders if total_orders > 0 else 0
        
        # Par fournisseur
        by_supplier = {}
        for order in period_orders:
            supplier_id = order.get("supplier_id")
            if supplier_id:
                if supplier_id not in by_supplier:
                    by_supplier[supplier_id] = {
                        "supplier_id": supplier_id,
                        "total": 0,
                        "orders_count": 0
                    }
                by_supplier[supplier_id]["total"] += order.get("total", 0)
                by_supplier[supplier_id]["orders_count"] += 1
        
        return {
            "period_months": period_months,
            "total_spent": total_spent,
            "total_orders": total_orders,
            "avg_order_value": avg_order_value,
            "by_supplier": list(by_supplier.values())
        }
    
    @staticmethod
    def calculate_savings(
        current_price: float,
        previous_price: float,
        quantity: int
    ) -> Dict:
        """
        Calcule les économies.
        
        Args:
            current_price: Prix actuel
            previous_price: Prix précédent
            quantity: Quantité
        
        Returns:
            Économies
        """
        unit_savings = previous_price - current_price
        total_savings = unit_savings * quantity
        savings_percent = (unit_savings / previous_price * 100) if previous_price > 0 else 0
        
        return {
            "unit_savings": unit_savings,
            "total_savings": total_savings,
            "savings_percent": savings_percent,
            "is_savings": total_savings > 0
        }


class ContractManager:
    """Gestionnaire de contrats"""
    
    @staticmethod
    def check_contract_expiry(
        contract: Dict,
        warning_days: int = 30
    ) -> Dict:
        """
        Vérifie l'expiration du contrat.
        
        Args:
            contrat: Contrat
            warning_days: Jours d'avertissement
        
        Returns:
            Statut
        """
        end_date = contract.get("end_date")
        now = datetime.now()
        
        days_until_expiry = (end_date - now).days if end_date else 0
        
        is_expiring = days_until_expiry <= warning_days
        is_expired = days_until_expiry < 0
        
        return {
            "is_expired": is_expired,
            "is_expiring": is_expiring,
            "days_until_expiry": days_until_expiry,
            "status": "expire" if is_expired else \
                     "expiring_soon" if is_expiring else "active"
        }


def generate_purchasing_report(
    purchase_orders: List[Dict],
    suppliers: List[Dict],
    period_start: datetime,
    period_end: datetime
) -> Dict:
    """
    Génère un rapport d'approvisionnement.
    
    Args:
        orders: Commandes
        suppliers: Fournisseurs
        start: Début
        end: Fin
    
    Returns:
        Rapport
    """
    period_orders = [
        o for o in purchase_orders
        if start <= o.get("created_at", datetime.min) <= end
    ]
    
    total_spent = sum(o.get("total", 0) for o in period_orders)
    pending = sum(1 for o in period_orders if o.get("status") == "en_attente")
    received = sum(1 for o in period_orders if o.get("status") == "recue")
    
    return {
        "period": {
            "start": period_start,
            "end": period_end
        },
        "total_orders": len(period_orders),
        "total_spent": total_spent,
        "pending_orders": pending,
        "received_orders": received,
        "active_suppliers": len(suppliers),
        "generated_at": datetime.now()
    }
