"""
Configuration du module banque

Ce module contient les configurations et utilitaires
pour le module de gestion bancaire.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from typing import List, Dict
from datetime import datetime, timedelta


class AccountManager:
    """Gestionnaire de comptes bancaires"""
    
    @staticmethod
    def calculate_interest(
        balance: float,
        rate: float,
        period_days: int
    ) -> float:
        """
        Calcule les intérêts.
        
        Args:
            balance: Solde
            rate: Taux d'intérêt
            period_days: Période en jours
        
        Returns:
            Intérêts
        """
        return balance * (rate / 100) * (period_days / 365)
    
    @staticmethod
    def check_overdraft(
        balance: float,
        overdraft_limit: float
    ) -> Dict:
        """
        Vérifie le découvert.
        
        Args:
            balance: Solde
            overdraft_limit: Limite de découvert
        
        Returns:
            Statut
        """
        is_overdrawn = balance < 0
        overdraft_amount = abs(balance) if is_overdrawn else 0
        available = balance + overdraft_limit
        
        return {
            "is_overdrawn": is_overdrawn,
            "overdraft_amount": overdraft_amount,
            "overdraft_limit": overdraft_limit,
            "available": available,
            "overdraft_percent": (overdraft_amount / overdraft_limit * 100) 
                                 if overdraft_limit > 0 else 0
        }


class TransactionProcessor:
    """Processeur de transactions"""
    
    @staticmethod
    def process_transfer(
        from_account: str,
        to_account: str,
        amount: float,
        description: str
    ) -> Dict:
        """
        Traite un virement.
        
        Args:
            from_account: Compte source
            to_account: Compte destination
            amount: Montant
            description: Description
        
        Returns:
            Transaction
        """
        return {
            "type": "transfer",
            "from_account": from_account,
            "to_account": to_account,
            "amount": amount,
            "description": description,
            "processed_at": datetime.now(),
            "status": "completed"
        }
    
    @staticmethod
    def calculate_fees(
        amount: float,
        transaction_type: str
    ) -> float:
        """
        Calcule les frais de transaction.
        
        Args:
            amount: Montant
            type: Type de transaction
        
        Returns:
            Frais
        """
        fees = {
            "virement_interne": 0,
            "virement_externe": 500,
            "retrait_guichet": 400,
            "carte": 100
        }
        
        return fees.get(transaction_type, 500)


class LoanCalculator:
    """Calculateur de prêts"""
    
    @staticmethod
    def calculate_monthly_payment(
        principal: float,
        annual_rate: float,
        months: int
    ) -> float:
        """
        Calcule la mensualité.
        
        Args:
            principal: Capital
            annual_rate: Taux annuel
            months: Durée en mois
        
        Returns:
            Mensualité
        """
        monthly_rate = annual_rate / 12 / 100
        
        if monthly_rate == 0:
            return principal / months
        
        payment = principal * (monthly_rate * (1 + monthly_rate) ** months) / \
                  ((1 + monthly_rate) ** months - 1)
        
        return payment
    
    @staticmethod
    def calculate_total_interest(
        principal: float,
        monthly_payment: float,
        months: int
    ) -> float:
        """
        Calcule le total des intérêts.
        
        Args:
            principal: Capital
            monthly_payment: Mensualité
            months: Durée en mois
        
        Returns:
            Total intérêts
        """
        total_paid = monthly_payment * months
        return total_paid - principal


class StatementGenerator:
    """Générateur de relevés"""
    
    @staticmethod
    def generate_monthly_statement(
        account: Dict,
        transactions: List[Dict],
        month: int,
        year: int
    ) -> Dict:
        """
        Génère un relevé mensuel.
        
        Args:
            account: Compte
            transactions: Transactions
            month: Mois
            year: Année
        
        Returns:
            Relevé
        """
        credits = [t for t in transactions 
                   if t.get("type") == "credit" 
                   and t["date"].month == month 
                   and t["date"].year == year]
        
        debits = [t for t in transactions 
                  if t.get("type") == "debit" 
                  and t["date"].month == month 
                  and t["date"].year == year]
        
        return {
            "account": account,
            "period": {"month": month, "year": year},
            "credits": {
                "count": len(credits),
                "total": sum(c.get("amount", 0) for c in credits)
            },
            "debits": {
                "count": len(debits),
                "total": sum(d.get("amount", 0) for d in debits)
            },
            "generated_at": datetime.now()
        }


class RiskAssessment:
    """Évaluation des risques"""
    
    @staticmethod
    def assess_credit_risk(
        income: float,
        expenses: float,
        existing_debts: float,
        credit_amount: float
    ) -> Dict:
        """
        Évalue le risque de crédit.
        
        Args:
            income: Revenu
            expenses: Dépenses
            existing_debts: Dettes existantes
            credit_amount: Montant demandé
        
        Returns:
            Évaluation
        """
        disposable_income = income - expenses - existing_debts
        debt_to_income = (existing_debts / income * 100) if income > 0 else 100
        new_debt_to_income = (credit_amount / income * 100) if income > 0 else 100
        
        # Score de risque
        risk_score = 0
        
        if debt_to_income > 40:
            risk_score += 3
        elif debt_to_income > 30:
            risk_score += 2
        elif debt_to_income > 20:
            risk_score += 1
        
        if new_debt_to_income > 30:
            risk_score += 2
        
        if disposable_income < 0:
            risk_score += 3
        
        # Niveau de risque
        if risk_score >= 5:
            risk_level = "tres_eleve"
        elif risk_score >= 3:
            risk_level = "eleve"
        elif risk_score >= 1:
            risk_level = "moyen"
        else:
            risk_level = "faible"
        
        return {
            "risk_score": risk_score,
            "risk_level": risk_level,
            "debt_to_income": debt_to_income,
            "disposable_income": disposable_income,
            "recommended": risk_score < 3
        }


class FraudDetection:
    """Détection de fraude"""
    
    @staticmethod
    def analyze_transaction_pattern(
        transactions: List[Dict],
        new_transaction: Dict
    ) -> Dict:
        """
        Analyse les patterns de transaction.
        
        Args:
            transactions: Transactions historiques
            new_transaction: Nouvelle transaction
        
        Returns:
            Analyse
        """
        if not transactions:
            return {"suspicious": False, "reason": "no_history"}
        
        # Calculer la moyenne et l'écart type
        amounts = [t.get("amount", 0) for t in transactions]
        avg_amount = sum(amounts) / len(amounts)
        
        # Vérifier si le montant est aberrant
        if new_transaction.get("amount", 0) > avg_amount * 3:
            return {
                "suspicious": True,
                "reason": "amount_anomaly",
                "avg_amount": avg_amount
            }
        
        # Vérifier la fréquence
        recent_transactions = [
            t for t in transactions
            if (datetime.now() - t.get("date", datetime.now())).days < 1
        ]
        
        if len(recent_transactions) > 10:
            return {
                "suspicious": True,
                "reason": "high_frequency"
            }
        
        return {"suspicious": False}


def generate_account_summary(
    account: Dict,
    transactions: List[Dict]
) -> Dict:
    """
    Génère un résumé de compte.
    
    Args:
        account: Compte
        transactions: Transactions
    
    Returns:
        Résumé
    """
    balance = sum(
        t.get("amount", 0) if t.get("type") == "credit" else -t.get("amount", 0)
        for t in transactions
    )
    
    return {
        "account": account,
        "balance": balance,
        "total_transactions": len(transactions),
        "generated_at": datetime.now()
    }
