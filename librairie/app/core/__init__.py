"""
Configuration du module librairie

Ce module contient les configurations et utilitaires
pour le module de gestion de librairie.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from typing import List, Dict
from datetime import datetime, timedelta


class BookManager:
    """Gestionnaire de livres"""
    
    @staticmethod
    def categorize_book(
        book: Dict
    ) -> str:
        """
        Catégorise un livre.
        
        Args:
            book: Livre
        
        Returns:
            Catégorie
        """
        genre = book.get("genre", "").lower()
        
        if genre in ["roman", "nouvelle", "recit"]:
            return "fiction"
        elif genre in ["manuel", "guide", "tutoriel"]:
            return "education"
        elif genre in ["science", "physique", "chimie", "biologie"]:
            return "science"
        elif genre in ["histoire", "biographie", "memoire"]:
            return "histoire"
        elif genre in ["poeme", "poesie"]:
            return "poesie"
        else:
            return "autre"
    
    @staticmethod
    def calculate_book_value(
        books: List[Dict]
    ) -> float:
        """
        Calcule la valeur totale du stock.
        
        Args:
            books: Livres
        
        Returns:
            Valeur
        """
        total = 0
        
        for book in books:
            quantity = book.get("quantity", 0)
            price = book.get("price", 0)
            total += quantity * price
        
        return total


class LendingManager:
    """Gestionnaire de prêts"""
    
    @staticmethod
    def create_loan(
        book_id: int,
        borrower_id: int,
        loan_days: int = 14
    ) -> Dict:
        """
        Crée un prêt.
        
        Args:
            book_id: ID livre
            borrower_id: ID emprunteur
            days: Durée du prêt
        
        Returns:
            Prêt
        """
        return {
            "book_id": book_id,
            "borrower_id": borrower_id,
            "loan_date": datetime.now(),
            "due_date": datetime.now() + timedelta(days=loan_days),
            "status": "actif",
            "renewals": 0
        }
    
    @staticmethod
    def check_due_date(
        loan: Dict
    ) -> Dict:
        """
        Vérifie la date d'échéance.
        
        Args:
            loan: Prêt
        
        Returns:
            Statut
        """
        due_date = loan.get("due_date")
        now = datetime.now()
        
        days_overdue = (now - due_date).days if due_date else 0
        
        if days_overdue > 0:
            status = "en_retard"
        elif days_overdue == 0:
            status = "due_aujourd_hui"
        else:
            status = "actif"
        
        return {
            "status": status,
            "days_overdue": max(0, days_overdue),
            "is_overdue": days_overdue > 0
        }
    
    @staticmethod
    def renew_loan(
        loan: Dict,
        additional_days: int = 14
    ) -> Dict:
        """
        Renouvelle un prêt.
        
        Args:
            loan: Prêt
            days: Jours supplémentaires
        
        Returns:
            Prêt renouvelé
        """
        max_renewals = 2
        current_renewals = loan.get("renewals", 0)
        
        if current_renewals >= max_renewals:
            return {
                "success": False,
                "reason": "renewal_limit_reached"
            }
        
        loan["due_date"] = loan.get("due_date") + timedelta(days=additional_days)
        loan["renewals"] = current_renewals + 1
        
        return {
            "success": True,
            "loan": loan
        }


class MemberManager:
    """Gestionnaire de membres"""
    
    @staticmethod
    def calculate_membership_fee(
        membership_type: str,
        duration_months: int = 12
    ) -> float:
        """
        Calcule la cotisation.
        
        Args:
            type: Type de membership
            duration: Durée en mois
        
        Returns:
            Cotisation
        """
        monthly_rates = {
            "standard": 5000,
            "premium": 10000,
            "etudiant": 2500,
            "famille": 15000
        }
        
        rate = monthly_rates.get(membership_type, 5000)
        return rate * duration_months
    
    @staticmethod
    def check_borrowing_limits(
        member: Dict,
        current_loans: int
    ) -> Dict:
        """
        Vérifie les limites d'emprunt.
        
        Args:
            member: Membre
            loans: Emprunts actuels
        
        Returns:
            Statut
        """
        limits = {
            "standard": 3,
            "premium": 5,
            "etudiant": 2,
            "famille": 8
        }
        
        member_type = member.get("membership_type", "standard")
        limit = limits.get(member_type, 3)
        
        can_borrow = current_loans < limit
        remaining = limit - current_loans
        
        return {
            "can_borrow": can_borrow,
            "current_loans": current_loans,
            "limit": limit,
            "remaining": remaining
        }


class InventoryTracker:
    """Suivi d'inventaire"""
    
    @staticmethod
    def check_low_stock(
        books: List[Dict],
        threshold: int = 5
    ) -> List[Dict]:
        """
        Vérifie le stock bas.
        
        Args:
            books: Livres
            threshold: Seuil
        
        Returns:
            Livres en rupture
        """
        low_stock = []
        
        for book in books:
            if book.get("quantity", 0) <= threshold:
                low_stock.append({
                    "book_id": book.get("id"),
                    "title": book.get("title"),
                    "quantity": book.get("quantity"),
                    "threshold": threshold
                })
        
        return low_stock
    
    @staticmethod
    def get_books_by_category(
        books: List[Dict]
    ) -> Dict:
        """
        Groupe les livres par catégorie.
        
        Args:
            books: Livres
        
        Returns:
            Catégories
        """
        categories = {}
        
        for book in books:
            category = BookManager.categorize_book(book)
            
            if category not in categories:
                categories[category] = []
            
            categories[category].append(book)
        
        return {
            category: len(books)
            for category, books in categories.items()
        }


class FineCalculator:
    """Calculateur d'amendes"""
    
    @staticmethod
    def calculate_late_fee(
        days_overdue: int,
        daily_rate: float = 200
    ) -> float:
        """
        Calcule l'amende de retard.
        
        Args:
            days_overdue: Jours de retard
            daily_rate: Taux journalier
        
        Returns:
            Amende
        """
        if days_overdue <= 0:
            return 0
        
        return days_overdue * daily_rate
    
    @staticmethod
    def calculate_damage_fee(
        damage_level: str
    ) -> float:
        """
        Calcule l'amende pour dommage.
        
        Args:
            level: Niveau de dommage
        
        Returns:
            Amende
        """
        damage_fees = {
            "legers": 1000,
            "moyens": 5000,
            "graves": 15000,
            "perdu": 25000
        }
        
        return damage_fees.get(damage_level, 0)


class ReportGenerator:
    """Générateur de rapports"""
    
    @staticmethod
    def generate_library_report(
        books: List[Dict],
        loans: List[Dict],
        members: List[Dict]
    ) -> Dict:
        """
        Génère un rapport de librairie.
        
        Args:
            books: Livres
            loans: Prêts
            members: Membres
        
        Returns:
            Rapport
        """
        total_books = len(books)
        total_value = BookManager.calculate_book_value(books)
        active_loans = sum(1 for l in loans if l.get("status") == "actif")
        overdue_loans = sum(
            1 for l in loans 
            if l.get("status") == "actif" 
            and l.get("due_date") < datetime.now()
        )
        
        low_stock = InventoryTracker.check_low_stock(books)
        
        return {
            "total_books": total_books,
            "total_value": total_value,
            "active_loans": active_loans,
            "overdue_loans": overdue_loans,
            "total_members": len(members),
            "low_stock_books": len(low_stock),
            "low_stock_list": low_stock,
            "generated_at": datetime.now()
        }
    
    @staticmethod
    def generate_member_report(
        member: Dict,
        loans: List[Dict]
    ) -> Dict:
        """
        Génère un rapport de membre.
        
        Args:
            member: Membre
            loans: Prêts
        
        Returns:
            Rapport
        """
        member_loans = [l for l in loans if l.get("borrower_id") == member.get("id")]
        active_loans = [l for l in member_loans if l.get("status") == "actif"]
        
        # Historique
        total_borrowed = len(member_loans)
        returned_on_time = sum(
            1 for l in member_loans
            if l.get("status") == "retourne"
            and l.get("return_date") <= l.get("due_date")
        )
        
        on_time_rate = (returned_on_time / total_borrowed * 100) if total_borrowed > 0 else 100
        
        return {
            "member": member,
            "total_borrowed": total_borrowed,
            "active_loans": len(active_loans),
            "on_time_rate": on_time_rate,
            "membership_type": member.get("membership_type"),
            "generated_at": datetime.now()
        }


def generate_borrowing_history(
    member_id: int,
    loans: List[Dict]
) -> Dict:
    """
    Génère l'historique d'emprunt.
    
    Args:
        member_id: ID membre
        loans: Prêts
    
    Returns:
        Historique
    """
    member_loans = [
        l for l in loans 
        if l.get("borrower_id") == member_id
    ]
    
    member_loans.sort(key=lambda x: x.get("loan_date", datetime.min), reverse=True)
    
    return {
        "member_id": member_id,
        "total_loans": len(member_loans),
        "loans": member_loans,
        "generated_at": datetime.now()
    }
