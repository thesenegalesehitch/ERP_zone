"""
Configuration du module gestion des stocks

Ce module contient les configurations et utilitaires
pour le module de gestion des stocks.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from typing import List, Dict
from datetime import datetime, timedelta


class InventoryManager:
    """Gestionnaire d'inventaire"""
    
    @staticmethod
    def calculate_stock_value(
        items: List[Dict],
        valuation_method: str = "fifo"
    ) -> float:
        """
        Calcule la valeur du stock.
        
        Args:
            items: Articles en stock
            method: Méthode d'évaluation (fifo, lifo, average)
        
        Returns:
            Valeur du stock
        """
        if not items:
            return 0.0
        
        if valuation_method == "fifo":
            # First In, First Out
            return sum(item.get("quantity", 0) * item.get("unit_cost", 0) 
                      for item in items)
        
        elif valuation_method == "lifo":
            # Last In, First Out
            sorted_items = sorted(items, key=lambda x: x.get("date", datetime.now()))
            return sum(item.get("quantity", 0) * item.get("unit_cost", 0) 
                      for item in sorted_items)
        
        elif valuation_method == "average":
            # Coût moyen
            total_cost = sum(
                item.get("quantity", 0) * item.get("unit_cost", 0) 
                for item in items
            )
            total_quantity = sum(item.get("quantity", 0) for item in items)
            return total_cost if total_quantity == 0 else total_cost / total_quantity * total_quantity
        
        return 0.0
    
    @staticmethod
    def check_reorder_point(
        current_stock: int,
        reorder_point: int,
        lead_time_days: int,
        daily_demand: int
    ) -> Dict:
        """
        Vérifie le point de réapprovisionnement.
        
        Args:
            current_stock: Stock actuel
            reorder_point: Point de réapprovisionnement
            lead_time_days: Délai de livraison
            daily_demand: Demande quotidienne
        
        Returns:
            Statut
        """
        days_until_stockout = current_stock / daily_demand if daily_demand > 0 else 999
        needs_reorder = current_stock <= reorder_point
        order_urgency = "critique" if days_until_stockout <= lead_time_days else \
                       "haute" if days_until_stockout <= lead_time_days * 1.5 else "normale"
        
        return {
            "needs_reorder": needs_reorder,
            "current_stock": current_stock,
            "reorder_point": reorder_point,
            "days_until_stockout": days_until_stockout,
            "urgency": order_urgency,
            "recommended_order_quantity": daily_demand * (lead_time_days + 7)
        }


class StockMovement:
    """Mouvements de stock"""
    
    @staticmethod
    def process_receipt(
        product_id: int,
        quantity: int,
        unit_cost: float,
        supplier: str,
        reference: str
    ) -> Dict:
        """
        Traite une réception de marchandise.
        
        Args:
            product_id: ID produit
            quantity: Quantité
            unit_cost: Coût unitaire
            supplier: Fournisseur
            reference: Référence
        
        Returns:
            Mouvement de stock
        """
        return {
            "type": "receipt",
            "product_id": product_id,
            "quantity": quantity,
            "unit_cost": unit_cost,
            "total_value": quantity * unit_cost,
            "supplier": supplier,
            "reference": reference,
            "processed_at": datetime.now()
        }
    
    @staticmethod
    def process_issue(
        product_id: int,
        quantity: int,
        destination: str,
        reference: str
    ) -> Dict:
        """
        Traite une sortie de marchandise.
        
        Args:
            product_id: ID produit
            quantity: Quantité
            destination: Destination
            reference: Référence
        
        Returns:
            Mouvement de stock
        """
        return {
            "type": "issue",
            "product_id": product_id,
            "quantity": quantity,
            "destination": destination,
            "reference": reference,
            "processed_at": datetime.now()
        }
    
    @staticmethod
    def process_adjustment(
        product_id: int,
        old_quantity: int,
        new_quantity: int,
        reason: str
    ) -> Dict:
        """
        Traite un ajustement de stock.
        
        Args:
            product_id: ID produit
            old_quantity: Ancienne quantité
            new_quantity: Nouvelle quantité
            reason: Raison
        
        Returns:
            Ajustement
        """
        difference = new_quantity - old_quantity
        
        return {
            "type": "adjustment",
            "product_id": product_id,
            "old_quantity": old_quantity,
            "new_quantity": new_quantity,
            "difference": difference,
            "reason": reason,
            "processed_at": datetime.now()
        }


class ABCAnalysis:
    """Analyse ABC des stocks"""
    
    @staticmethod
    def perform_abc_analysis(
        products: List[Dict],
        periods: int = 12
    ) -> Dict:
        """
        Effectue une analyse ABC.
        
        Args:
            products: Produits
            periods: Périodes à analyser
        
        Returns:
            Classification ABC
        """
        # Calculer la valeur annuelle pour chaque produit
        product_values = []
        
        for product in products:
            annual_value = product.get("annual_usage", 0) * product.get("unit_cost", 0)
            product_values.append({
                "product_id": product.get("id"),
                "name": product.get("name"),
                "annual_value": annual_value
            })
        
        # Trier par valeur décroissante
        product_values.sort(key=lambda x: x["annual_value"], reverse=True)
        
        # Calculer le total
        total_value = sum(p["annual_value"] for p in product_values)
        
        # Classifier
        classified = {"A": [], "B": [], "C": []}
        cumulative_value = 0
        
        for product in product_values:
            cumulative_value += product["annual_value"]
            percent = (cumulative_value / total_value * 100) if total_value > 0 else 0
            
            if percent <= 80:
                classified["A"].append(product)
            elif percent <= 95:
                classified["B"].append(product)
            else:
                classified["C"].append(product)
        
        return {
            "classification": classified,
            "total_value": total_value,
            "analysis_date": datetime.now()
        }


class StockForecast:
    """Prévision des stocks"""
    
    @staticmethod
    def calculate_moving_average(
        historical_data: List[float],
        period: int = 3
    ) -> float:
        """
        Calcule la moyenne mobile.
        
        Args:
            historical_data: Données historiques
            period: Période
        
        Returns:
            Prévision
        """
        if len(historical_data) < period:
            return sum(historical_data) / len(historical_data) if historical_data else 0
        
        recent = historical_data[-period:]
        return sum(recent) / period
    
    @staticmethod
    def calculate_safety_stock(
        avg_daily_usage: float,
        lead_time_days: int,
        service_level: float = 0.95
    ) -> float:
        """
        Calcule le stock de sécurité.
        
        Args:
            avg_daily_usage: Utilisation quotidienne moyenne
            lead_time_days: Délai de livraison
            service_level: Niveau de service
        
        Returns:
            Stock de sécurité
        """
        # Facteur de sécurité selon le niveau de service
        z_scores = {
            0.90: 1.28,
            0.95: 1.65,
            0.99: 2.33
        }
        
        z = z_scores.get(service_level, 1.65)
        
        # Calculer l'écart type de la demande
        safety_stock = z * (avg_daily_usage * lead_time_days) ** 0.5
        
        return safety_stock


class ExpiryTracker:
    """Suivi des dates d'expiration"""
    
    @staticmethod
    def check_expiring_items(
        items: List[Dict],
        warning_days: int = 30
    ) -> Dict:
        """
        Vérifie les articles expirants.
        
        Args:
            items: Articles
            warning_days: Jours d'avertissement
        
        Returns:
            Statut d'expiration
        """
        now = datetime.now()
        expiring_soon = []
        expired = []
        valid = []
        
        for item in items:
            expiry_date = item.get("expiry_date")
            
            if not expiry_date:
                valid.append(item)
                continue
            
            days_until_expiry = (expiry_date - now).days
            
            if days_until_expiry < 0:
                expired.append({**item, "days_expired": abs(days_until_expiry)})
            elif days_until_expiry <= warning_days:
                expiring_soon.append({**item, "days_until_expiry": days_until_expiry})
            else:
                valid.append(item)
        
        return {
            "expired": expired,
            "expiring_soon": expiring_soon,
            "valid": valid,
            "summary": {
                "expired_count": len(expired),
                "expiring_soon_count": len(expiring_soon),
                "valid_count": len(valid)
            }
        }


def generate_inventory_report(
    products: List[Dict],
    movements: List[Dict]
) -> Dict:
    """
    Génère un rapport d'inventaire.
    
    Args:
        products: Produits
        movements: Mouvements
    
    Returns:
        Rapport
    """
    total_value = InventoryManager.calculate_stock_value(products)
    low_stock = [p for p in products if p.get("quantity", 0) <= p.get("reorder_point", 0)]
    
    return {
        "total_products": len(products),
        "total_value": total_value,
        "low_stock_count": len(low_stock),
        "low_stock_items": low_stock,
        "generated_at": datetime.now()
    }
