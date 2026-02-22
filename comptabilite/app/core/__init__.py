"""
Configuration du module comptabilité

Ce module contient les configurations et utilitaires
pour le module de comptabilité.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from typing import List, Dict
from datetime import datetime, timedelta
from decimal import Decimal


class InvoiceManager:
    """Gestionnaire de factures"""
    
    @staticmethod
    def calculate_total(
        items: List[Dict],
        tax_rate: float = 0.0
    ) -> Dict:
        """
        Calcule le total de la facture.
        
        Args:
            items: Articles
            tax_rate: Taux de taxe
        
        Returns:
            Totaux
        """
        subtotal = sum(
            item.get("quantity", 0) * item.get("unit_price", 0)
            for item in items
        )
        tax_amount = subtotal * (tax_rate / 100)
        total = subtotal + tax_amount
        
        return {
            "subtotal": subtotal,
            "tax_amount": tax_amount,
            "total": total,
            "tax_rate": tax_rate
        }
    
    @staticmethod
    def get_invoice_status(days_overdue: int) -> str:
        """
        Détermine le statut de la facture.
        
        Args:
            days_overdue: Jours de retard
        
        Returns:
            Statut
        """
        if days_overdue <= 0:
            return "a_time"
        elif days_overdue <= 30:
            return "en_retard"
        elif days_overdue <= 60:
            return "tres_en_retard"
        else:
            return "impayee"


class PaymentProcessor:
    """Processeur de paiement"""
    
    @staticmethod
    def process_payment(
        amount: float,
        payment_method: str,
        reference: str
    ) -> Dict:
        """
        Traite un paiement.
        
        Args:
            amount: Montant
            payment_method: Méthode de paiement
            reference: Référence
        
        Returns:
            Résultat
        """
        return {
            "amount": amount,
            "method": payment_method,
            "reference": reference,
            "processed_at": datetime.now(),
            "status": "completed"
        }
    
    @staticmethod
    def calculate_fees(
        amount: float,
        method: str
    ) -> float:
        """
        Calcule les frais de transaction.
        
        Args:
            amount: Montant
            method: Méthode
        
        Returns:
            Frais
        """
        fees_rates = {
            "carte_bancaire": 1.4,
            "virement": 0.5,
            "cheque": 0.3,
            "especes": 0.0
        }
        
        rate = fees_rates.get(method, 1.0)
        return amount * (rate / 100)


class AccountManager:
    """Gestionnaire de comptes"""
    
    @staticmethod
    def calculate_balance(
        transactions: List[Dict]
    ) -> float:
        """
        Calcule le solde du compte.
        
        Args:
            transactions: Transactions
        
        Returns:
            Solde
        """
        balance = 0.0
        
        for transaction in transactions:
            if transaction.get("type") == "credit":
                balance += transaction.get("amount", 0)
            elif transaction.get("type") == "debit":
                balance -= transaction.get("amount", 0)
        
        return balance
    
    @staticmethod
    def get_account_type(account_number: str) -> str:
        """
        Détermine le type de compte.
        
        Args:
            account_number: Numéro de compte
        
        Returns:
            Type
        """
        if account_number.startswith("4"):
            return "actif"
        elif account_number.startswith("5"):
            return "passif"
        elif account_number.startswith("6"):
            return "charge"
        elif account_number.startswith("7"):
            return "produit"
        else:
            return "autre"


class TaxCalculator:
    """Calculateur de taxes"""
    
    @staticmethod
    def calculate_tva(
        amount: float,
        rate: float = 18.0
    ) -> Dict:
        """
        Calcule la TVA.
        
        Args:
            amount: Montant
            rate: Taux
        
        Returns:
            Détails TVA
        """
        vat_amount = amount * (rate / 100)
        total = amount + vat_amount
        
        return {
            "ht": amount,
            "tva_rate": rate,
            "tva_amount": vat_amount,
            "ttc": total
        }
    
    @staticmethod
    def calculate_withholding(
        amount: float,
        rate: float
    ) -> float:
        """
        Calcule la retenue à la source.
        
        Args:
            amount: Montant
            rate: Taux
        
        Returns:
            Retenue
        """
        return amount * (rate / 100)


class FinancialReport:
    """Rapport financier"""
    
    @staticmethod
    def generate_balance_sheet(
        assets: List[Dict],
        liabilities: List[Dict],
        equity: List[Dict]
    ) -> Dict:
        """
        Génère le bilan.
        
        Args:
            assets: Actifs
            liabilities: Passifs
            equity: Capitaux propres
        
        Returns:
            Bilan
        """
        total_assets = sum(a.get("value", 0) for a in assets)
        total_liabilities = sum(l.get("value", 0) for l in liabilities)
        total_equity = sum(e.get("value", 0) for e in equity)
        
        return {
            "assets": {
                "items": assets,
                "total": total_assets
            },
            "liabilities": {
                "items": liabilities,
                "total": total_liabilities
            },
            "equity": {
                "items": equity,
                "total": total_equity
            },
            "generated_at": datetime.now()
        }
    
    @staticmethod
    def generate_income_statement(
        revenues: List[Dict],
        expenses: List[Dict]
    ) -> Dict:
        """
        Génère le compte de résultat.
        
        Args:
            revenues: Revenus
            expenses: Dépenses
        
        Returns:
            Compte de résultat
        """
        total_revenues = sum(r.get("amount", 0) for r in revenues)
        total_expenses = sum(e.get("amount", 0) for e in expenses)
        net_result = total_revenues - total_expenses
        
        return {
            "revenues": {
                "items": revenues,
                "total": total_revenues
            },
            "expenses": {
                "items": expenses,
                "total": total_expenses
            },
            "net_result": net_result,
            "generated_at": datetime.now()
        }


class BudgetTracker:
    """Suivi budgétaire"""
    
    @staticmethod
    def calculate_variance(
        budgeted: float,
        actual: float
    ) -> Dict:
        """
        Calcule l'écart budgétaire.
        
        Args:
            budgeted: Budgété
            actual: Réel
        
        Returns:
            Écart
        """
        variance = actual - budgeted
        variance_percent = (variance / budgeted * 100) if budgeted != 0 else 0
        
        return {
            "budgeted": budgeted,
            "actual": actual,
            "variance": variance,
            "variance_percent": variance_percent,
            "is_over_budget": variance > 0
        }


def generate_financial_summary(
    transactions: List[Dict],
    start_date: datetime,
    end_date: datetime
) -> Dict:
    """
    Génère un résumé financier.
    
    Args:
        transactions: Transactions
        start_date: Date de début
        end_date: Date de fin
    
    Returns:
        Résumé
    """
    credits = [t for t in transactions if t.get("type") == "credit"]
    debits = [t for t in transactions if t.get("type") == "debit"]
    
    total_credits = sum(c.get("amount", 0) for c in credits)
    total_debits = sum(d.get("amount", 0) for d in debits)
    
    return {
        "period": {
            "start": start_date,
            "end": end_date
        },
        "credits": {
            "count": len(credits),
            "total": total_credits
        },
        "debits": {
            "count": len(debits),
            "total": total_debits
        },
        "net": total_credits - total_debits,
        "generated_at": datetime.now()
    }
