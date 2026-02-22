"""
Configuration du module point de vente

Ce module contient les configurations et utilitaires
pour le module de point de vente (POS).

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from typing import List, Dict
from datetime import datetime, timedelta


class POSManager:
    """Gestionnaire de point de vente"""
    
    @staticmethod
    def create_sale(
        items: List[Dict],
        customer_id: int = None,
        payment_method: str = "especes"
    ) -> Dict:
        """
        Crée une vente.
        
        Args:
            items: Articles
            customer_id: ID client
            payment_method: Mode de paiement
        
        Returns:
            Vente
        """
        subtotal = sum(item.get("quantity", 0) * item.get("price", 0) for item in items)
        
        return {
            "items": items,
            "customer_id": customer_id,
            "payment_method": payment_method,
            "subtotal": subtotal,
            "tax": subtotal * 0.18,  # TVA 18%
            "total": subtotal * 1.18,
            "status": "terminee",
            "created_at": datetime.now()
        }
    
    @staticmethod
    def calculate_change(
        amount_paid: float,
        total: float
    ) -> float:
        """
        Calcule la monnaie.
        
        Args:
            amount_paid: Montant payé
            total: Total
        
        Returns:
            Monnaie
        """
        return amount_paid - total if amount_paid >= total else 0


class CartManager:
    """Gestionnaire de panier"""
    
    @staticmethod
    def add_item(
        cart: List[Dict],
        product_id: int,
        quantity: int,
        price: float
    ) -> List[Dict]:
        """
        Ajoute un article au panier.
        
        Args:
            cart: Panier
            product_id: ID produit
            quantity: Quantité
            price: Prix
        
        Returns:
            Panier mis à jour
        """
        # Vérifier si le produit existe déjà
        for item in cart:
            if item.get("product_id") == product_id:
                item["quantity"] += quantity
                return cart
        
        # Ajouter nouveau produit
        cart.append({
            "product_id": product_id,
            "quantity": quantity,
            "price": price
        })
        
        return cart
    
    @staticmethod
    def calculate_cart_total(
        cart: List[Dict],
        discount_percent: float = 0
    ) -> Dict:
        """
        Calcule le total du panier.
        
        Args:
            cart: Panier
            discount_percent: Pourcentage de remise
        
        Returns:
            Total
        """
        subtotal = sum(item.get("quantity", 0) * item.get("price", 0) for item in cart)
        discount = subtotal * (discount_percent / 100)
        after_discount = subtotal - discount
        tax = after_discount * 0.18
        total = after_discount + tax
        
        return {
            "subtotal": subtotal,
            "discount": discount,
            "after_discount": after_discount,
            "tax": tax,
            "total": total,
            "item_count": len(cart)
        }


class InventorySync:
    """Synchronisation d'inventaire"""
    
    @staticmethod
    def check_availability(
        product_id: int,
        requested_quantity: int,
        available_stock: int
    ) -> Dict:
        """
        Vérifie la disponibilité.
        
        Args:
            product_id: ID produit
            quantity: Quantité demandée
            stock: Stock disponible
        
        Returns:
            Disponibilité
        """
        is_available = available_stock >= requested_quantity
        
        return {
            "product_id": product_id,
            "requested": requested_quantity,
            "available": available_stock,
            "is_available": is_available,
            "can_partial": available_stock > 0
        }
    
    @staticmethod
    def reserve_stock(
        product_id: int,
        quantity: int,
        current_stock: int
    ) -> Dict:
        """
        Réserve le stock.
        
        Args:
            product_id: ID produit
            quantity: Quantité
            stock: Stock actuel
        
        Returns:
            Réservation
        """
        if current_stock >= quantity:
            return {
                "success": True,
                "new_stock": current_stock - quantity,
                "reserved": quantity
            }
        
        return {
            "success": False,
            "new_stock": current_stock,
            "reserved": 0,
            "reason": "insufficient_stock"
        }


class DiscountManager:
    """Gestionnaire de remises"""
    
    @staticmethod
    def calculate_discount(
        amount: float,
        discount_type: str,
        discount_value: float,
        conditions: Dict = None
    ) -> float:
        """
        Calcule la remise.
        
        Args:
            amount: Montant
            type: Type de remise (percent, fixed)
            value: Valeur
            conditions: Conditions
        
        Returns:
            Montant de la remise
        """
        # Vérifier les conditions
        if conditions:
            min_purchase = conditions.get("min_purchase", 0)
            if amount < min_purchase:
                return 0
        
        if discount_type == "percent":
            return amount * (discount_value / 100)
        elif discount_type == "fixed":
            return min(discount_value, amount)
        
        return 0
    
    @staticmethod
    def apply_loyalty_discount(
        customer_points: int,
        total: float
    ) -> Dict:
        """
        Applique la remise fidélité.
        
        Args:
            points: Points de fidélité
            total: Total
        
        Returns:
            Remise
        """
        # 100 points = 1000 XOF de remise
        discount_value = (customer_points // 100) * 1000
        discount_value = min(discount_value, total * 0.2)  # Max 20%
        
        return {
            "points_used": (discount_value // 1000) * 100,
            "discount": discount_value,
            "remaining_points": customer_points - ((discount_value // 1000) * 100)
        }


class ReceiptGenerator:
    """Générateur de reçus"""
    
    @staticmethod
    def generate_receipt(
        sale: Dict,
        store_info: Dict = None
    ) -> str:
        """
        Génère un reçu.
        
        Args:
            sale: Vente
            info: Info magasin
        
        Returns:
            Reçu formaté
        """
        receipt = []
        
        # En-tête
        receipt.append("=" * 40)
        receipt.append(store_info.get("name", "MON MAGASIN") if store_info else "MON MAGASIN")
        receipt.append(store_info.get("address", "") if store_info else "")
        receipt.append("=" * 40)
        receipt.append(f"Date: {sale.get('created_at').strftime('%d/%m/%Y %H:%M')}")
        receipt.append(f"Ticket: {sale.get('id', 'N/A')}")
        receipt.append("-" * 40)
        
        # Articles
        for item in sale.get("items", []):
            qty = item.get("quantity", 0)
            price = item.get("price", 0)
            total = qty * price
            receipt.append(f"{qty} x {price:,.0f} = {total:,.0f}")
        
        receipt.append("-" * 40)
        
        # Totaux
        receipt.append(f"Sous-total: {sale.get('subtotal', 0):,.0f}")
        receipt.append(f"TVA (18%): {sale.get('tax', 0):,.0f}")
        receipt.append(f"TOTAL: {sale.get('total', 0):,.0f}")
        
        if sale.get("payment_method"):
            receipt.append(f"Paiement: {sale.get('payment_method')}")
        
        receipt.append("=" * 40)
        receipt.append("Merci de votre achat!")
        receipt.append("À bientôt!")
        
        return "\n".join(receipt)


class SalesReport:
    """Rapport des ventes"""
    
    @staticmethod
    def generate_daily_summary(
        sales: List[Dict],
        date: datetime
    ) -> Dict:
        """
        Génère un résumé quotidien.
        
        Args:
            sales: Ventes
            date: Date
        
        Returns:
            Résumé
        """
        day_sales = [
            s for s in sales
            if s.get("created_at").date() == date.date()
        ]
        
        total_revenue = sum(s.get("total", 0) for s in day_sales)
        total_items = sum(
            sum(item.get("quantity", 0) for item in s.get("items", []))
            for s in day_sales
        )
        
        # Par méthode de paiement
        by_payment = {}
        for sale in day_sales:
            method = sale.get("payment_method", "autre")
            by_payment[method] = by_payment.get(method, 0) + sale.get("total", 0)
        
        return {
            "date": date,
            "total_sales": len(day_sales),
            "total_revenue": total_revenue,
            "total_items_sold": total_items,
            "average_sale": total_revenue / len(day_sales) if day_sales else 0,
            "by_payment_method": by_payment
        }
    
    @staticmethod
    def get_top_products(
        sales: List[Dict],
        limit: int = 10
    ) -> List[Dict]:
        """
        Obtient les produits vedettes.
        
        Args:
            sales: Ventes
            limit: Limite
        
        Returns:
            Top produits
        """
        product_sales = {}
        
        for sale in sales:
            for item in sale.get("items", []):
                product_id = item.get("product_id")
                quantity = item.get("quantity", 0)
                
                if product_id in product_sales:
                    product_sales[product_id]["quantity"] += quantity
                    product_sales[product_id]["revenue"] += quantity * item.get("price", 0)
                else:
                    product_sales[product_id] = {
                        "product_id": product_id,
                        "quantity": quantity,
                        "revenue": quantity * item.get("price", 0)
                    }
        
        # Trier par quantité
        sorted_products = sorted(
            product_sales.values(),
            key=lambda x: x.get("quantity", 0),
            reverse=True
        )
        
        return sorted_products[:limit]


def generate_pos_daily_report(
    sales: List[Dict],
    date: datetime,
    employees: List[Dict]
) -> Dict:
    """
    Génère un rapport quotidien POS.
    
    Args:
        sales: Ventes
        date: Date
        employees: Employés
    
    Returns:
        Rapport
    """
    summary = SalesReport.generate_daily_summary(sales, date)
    top_products = SalesReport.get_top_products(sales)
    
    # Ventes par employé
    sales_by_employee = {}
    for sale in sales:
        employee_id = sale.get("employee_id")
        if employee_id:
            if employee_id not in sales_by_employee:
                sales_by_employee[employee_id] = 0
            sales_by_employee[employee_id] += sale.get("total", 0)
    
    return {
        "date": date,
        "summary": summary,
        "top_products": top_products,
        "sales_by_employee": sales_by_employee,
        "generated_at": datetime.now()
    }
