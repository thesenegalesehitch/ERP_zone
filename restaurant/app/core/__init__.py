"""
Configuration du module restaurant

Ce module contient les configurations et utilitaires
pour le module de gestion de restaurant.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from typing import List, Dict
from datetime import datetime, timedelta


class TableManager:
    """Gestionnaire de tables"""
    
    @staticmethod
    def get_table_status(
        table_id: int,
        current_orders: List[Dict]
    ) -> Dict:
        """
        Obtient le statut d'une table.
        
        Args:
            table_id: ID table
            orders: Commandes en cours
        
        Returns:
            Statut
        """
        table_orders = [o for o in current_orders if o.get("table_id") == table_id]
        
        if not table_orders:
            return {
                "table_id": table_id,
                "status": "disponible",
                "current_order": None
            }
        
        # Vérifier si la commande est payée
        all_paid = all(o.get("status") == "payee" for o in table_orders)
        
        if all_paid:
            return {
                "table_id": table_id,
                "status": "disponible",
                "current_order": None
            }
        
        return {
            "table_id": table_id,
            "status": "occupyee",
            "current_order": table_orders[0] if table_orders else None,
            "order_total": sum(o.get("total", 0) for o in table_orders)
        }
    
    @staticmethod
    def reserve_table(
        table_id: int,
        customer_name: str,
        reservation_time: datetime,
        guest_count: int
    ) -> Dict:
        """
        Réserve une table.
        
        Args:
            table_id: ID table
            customer_name: Nom du client
            time: Heure de réservation
            guests: Nombre de convives
        
        Returns:
            Réservation
        """
        return {
            "table_id": table_id,
            "customer_name": customer_name,
            "reservation_time": reservation_time,
            "guest_count": guest_count,
            "status": "reservee",
            "created_at": datetime.now()
        }


class MenuManager:
    """Gestionnaire de menu"""
    
    @staticmethod
    def calculate_menu_item_cost(
        ingredients: List[Dict]
    ) -> float:
        """
        Calcule le coût d'un article.
        
        Args:
            ingredients: Ingrédients
        
        Returns:
            Coût
        """
        total_cost = 0
        
        for ingredient in ingredients:
            quantity = ingredient.get("quantity", 0)
            unit_cost = ingredient.get("unit_cost", 0)
            total_cost += quantity * unit_cost
        
        return total_cost
    
    @staticmethod
    def calculate_profit_margin(
        selling_price: float,
        cost: float
    ) -> Dict:
        """
        Calcule la marge bénéficiaire.
        
        Args:
            selling_price: Prix de vente
            cost: Coût
        
        Returns:
            Marge
        """
        profit = selling_price - cost
        margin_percent = (profit / selling_price * 100) if selling_price > 0 else 0
        
        return {
            "selling_price": selling_price,
            "cost": cost,
            "profit": profit,
            "margin_percent": margin_percent
        }
    
    @staticmethod
    def check_availability(
        menu_item_id: int,
        required_ingredients: List[Dict],
        inventory: Dict
    ) -> Dict:
        """
        Vérifie la disponibilité des ingrédients.
        
        Args:
            menu_item_id: ID article
            required: Ingrédients requis
            inventory: Inventaire
        
        Returns:
            Disponibilité
        """
        available = []
        unavailable = []
        
        for ingredient in required_ingredients:
            ingredient_id = ingredient.get("ingredient_id")
            required_qty = ingredient.get("quantity", 0)
            available_qty = inventory.get(ingredient_id, 0)
            
            if available_qty >= required_qty:
                available.append({
                    "ingredient_id": ingredient_id,
                    "required": required_qty,
                    "available": available_qty
                })
            else:
                unavailable.append({
                    "ingredient_id": ingredient_id,
                    "required": required_qty,
                    "available": available_qty
                })
        
        return {
            "available": len(unavailable) == 0,
            "can_make": available,
            "missing": unavailable
        }


class OrderManager:
    """Gestionnaire de commandes"""
    
    @staticmethod
    def create_order(
        table_id: int,
        items: List[Dict],
        waiter_id: int,
        order_type: str = "sur_place"
    ) -> Dict:
        """
        Crée une commande.
        
        Args:
            table_id: ID table
            items: Articles
            waiter_id: ID serveur
            type: Type de commande
        
        Returns:
            Commande
        """
        subtotal = sum(item.get("quantity", 0) * item.get("price", 0) for item in items)
        
        return {
            "table_id": table_id,
            "items": items,
            "waiter_id": waiter_id,
            "order_type": order_type,
            "subtotal": subtotal,
            "tax": subtotal * 0.18,
            "total": subtotal * 1.18,
            "status": "en_cours",
            "created_at": datetime.now()
        }
    
    @staticmethod
    def update_order_status(
        order: Dict,
        new_status: str
    ) -> Dict:
        """
        Met à jour le statut de la commande.
        
        Args:
            order: Commande
            status: Nouveau statut
        
        Returns:
            Commande mise à jour
        """
        status_flow = {
            "en_cours": ["prete", "annulee"],
            "prete": ["servie", "annulee"],
            "servie": ["payee"],
            "payee": [],
            "annulee": []
        }
        
        current_status = order.get("status")
        
        if new_status in status_flow.get(current_status, []):
            order["status"] = new_status
            
            if new_status == "servie":
                order["served_at"] = datetime.now()
            elif new_status == "payee":
                order["paid_at"] = datetime.now()
            
            return {
                "success": True,
                "order": order
            }
        
        return {
            "success": False,
            "reason": "invalid_status_transition"
        }


class KitchenManager:
    """Gestionnaire de cuisine"""
    
    @staticmethod
    def send_to_kitchen(
        order_id: int,
        items: List[Dict]
    ) -> Dict:
        """
        Envoie à la cuisine.
        
        Args:
            order_id: ID commande
            items: Articles
        
        Returns:
            Ticket cuisine
        """
        return {
            "order_id": order_id,
            "items": items,
            "priority": "normale",
            "sent_at": datetime.now(),
            "status": "en_preparation"
        }
    
    @staticmethod
    def mark_item_ready(
        ticket: Dict,
        item_id: int
    ) -> Dict:
        """
        Marque un article comme prêt.
        
        Args:
            ticket: Ticket
            item_id: ID article
        
        Returns:
            Ticket mis à jour
        """
        for item in ticket.get("items", []):
            if item.get("item_id") == item_id:
                item["status"] = "pret"
        
        # Vérifier si tout est prêt
        all_ready = all(
            i.get("status") == "pret" 
            for i in ticket.get("items", [])
        )
        
        if all_ready:
            ticket["status"] = "pret"
            ticket["ready_at"] = datetime.now()
        
        return ticket


class BillingManager:
    """Gestionnaire de facturation"""
    
    @staticmethod
    def split_bill(
        order: Dict,
        split_method: str,
        split_details: List[Dict]
    ) -> Dict:
        """
        Divise l'addition.
        
        Args:
            order: Commande
            method: Méthode de partage
            details: Détails du partage
        
        Returns:
            Divisions
        """
        total = order.get("total", 0)
        
        if split_method == "equal":
            count = len(split_details)
            per_person = total / count if count > 0 else 0
            
            return {
                "method": "equal",
                "per_person": per_person,
                "splits": [{"amount": per_person} for _ in split_details]
            }
        
        elif split_method == "custom":
            return {
                "method": "custom",
                "splits": split_details,
                "total": sum(s.get("amount", 0) for s in split_details)
            }
        
        return {"error": "invalid_method"}
    
    @staticmethod
    def apply_discount(
        order: Dict,
        discount_type: str,
        discount_value: float
    ) -> Dict:
        """
        Applique une remise.
        
        Args:
            order: Commande
            type: Type de remise
            value: Valeur
        
        Returns:
            Commande avec remise
        """
        subtotal = order.get("subtotal", 0)
        
        if discount_type == "percent":
            discount = subtotal * (discount_value / 100)
        elif discount_type == "fixed":
            discount = discount_value
        else:
            discount = 0
        
        new_subtotal = subtotal - discount
        new_tax = new_subtotal * 0.18
        new_total = new_subtotal + new_tax
        
        return {
            "original_subtotal": subtotal,
            "discount": discount,
            "new_subtotal": new_subtotal,
            "tax": new_tax,
            "total": new_total
        }


class AnalyticsManager:
    """Gestionnaire d'analytique"""
    
    @staticmethod
    def calculate_table_turnover(
        table_id: int,
        orders: List[Dict],
        period_hours: int = 8
    ) -> float:
        """
        Calcule le taux de rotation des tables.
        
        Args:
            table_id: ID table
            orders: Commandes
            period: Période en heures
        
        Returns:
            Rotation
        """
        now = datetime.now()
        period_start = now - timedelta(hours=period_hours)
        
        table_orders = [
            o for o in orders
            if o.get("table_id") == table_id
            and o.get("created_at") >= period_start
            and o.get("status") == "payee"
        ]
        
        return len(table_orders)
    
    @staticmethod
    def get_popular_items(
        orders: List[Dict],
        period_hours: int = 24
    ) -> List[Dict]:
        """
        Obtient les articles populaires.
        
        Args:
            orders: Commandes
            period: Période
        
        Returns:
            Articles populaires
        """
        now = datetime.now()
        period_start = now - timedelta(hours=period_hours)
        
        recent_orders = [
            o for o in orders
            if o.get("created_at") >= period_start
        ]
        
        item_counts = {}
        
        for order in recent_orders:
            for item in order.get("items", []):
                item_id = item.get("menu_item_id")
                if item_id:
                    if item_id not in item_counts:
                        item_counts[item_id] = {
                            "item_id": item_id,
                            "name": item.get("name"),
                            "quantity": 0,
                            "revenue": 0
                        }
                    item_counts[item_id]["quantity"] += item.get("quantity", 0)
                    item_counts[item_id]["revenue"] += item.get("quantity", 0) * item.get("price", 0)
        
        return sorted(
            item_counts.values(),
            key=lambda x: x.get("quantity", 0),
            reverse=True
        )


def generate_restaurant_report(
    orders: List[Dict],
    tables: List[Dict],
    period_start: datetime,
    period_end: datetime
) -> Dict:
    """
    Génère un rapport de restaurant.
    
    Args:
        orders: Commandes
        tables: Tables
        start: Début de période
        end: Fin de période
    
    Returns:
        Rapport
    """
    period_orders = [
        o for o in orders
        if start <= o.get("created_at") <= end
    ]
    
    total_revenue = sum(o.get("total", 0) for o in period_orders)
    total_orders = len(period_orders)
    
    avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
    
    popular = AnalyticsManager.get_popular_items(period_orders)
    
    return {
        "period": {
            "start": period_start,
            "end": period_end
        },
        "summary": {
            "total_orders": total_orders,
            "total_revenue": total_revenue,
            "avg_order_value": avg_order_value
        },
        "popular_items": popular[:10],
        "generated_at": datetime.now()
    }
