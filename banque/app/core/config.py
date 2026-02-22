"""
Configuration du module banque

Ce module contient la configuration du projet
pour le module de gestion bancaire.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""

# Configuration du module banque

# Paramètres de configuration
MODULE_NAME = "banque"
MODULE_VERSION = "1.0.0"

# Types de comptes bancaires
ACCOUNT_TYPES = [
    "compte_courant",
    "compte_epargne",
    "compte_blocage",
    "compte_devises"
]

# Types de transactions
TRANSACTION_TYPES = [
    "depot",
    "retrait",
    "virement_interne",
    "virement_externe",
    "prelevement",
    "cheque",
    "carte",
    "frais"
]

# Statuts de transaction
TRANSACTION_STATUS = [
    "en_attente",
    "validee",
    "rejetee",
    "annulee"
]

# Types de prêts
LOAN_TYPES = [
    "conso",
    "immobilier",
    "professionnel",
    "urgence",
    "scolaire"
]

# Statuts de prêt
LOAN_STATUS = [
    "en_cours",
    "approuve",
    "rejete",
    "termine",
    "defaut"
]

# Types de cartes
CARD_TYPES = [
    "debit",
    "credit",
    "prepayee"
]

# Statuts de carte
CARD_STATUS = [
    "active",
    "bloquee",
    "expiree",
    "annulee"
]

# Configuration des intérêts
INTEREST_CONFIG = {
    "compte_epargne": {
        "rate": 3.5,
        "compound_frequency": "annual"
    },
    "compte_courant": {
        "rate": 0,
        "overdraft_rate": 15.0
    }
}

# Frais bancaires
BANKING_FEES = {
    "virement_interne": 0,
    "virement_externe": 500,
    "retrait_guichet": 400,
    "retrait_dab": 200,
    "carte_annuelle": 5000,
    "tenue_compte": 2500,
    "agios": 0.02  # Taux journalier
}

# Configuration des prêts
LOAN_CONFIG = {
    "max_amount": 50000000,
    "min_amount": 100000,
    "max_term_months": 120,
    "min_term_months": 3,
    "interest_rate": 10.0,
    "insurance_rate": 0.5
}

# Garanties
GUARANTEE_TYPES = [
    "salaire",
    "hypotheque",
    "gage",
    "caution",
    "assurance"
]

# Configuration des alertes
ALERT_CONFIG = {
    "low_balance": 50000,
    "large_transaction": 1000000,
    "suspicious_activity": True
}

# Rôles et permissions
ROLE_PERMISSIONS = {
    "admin_banque": [
        "account_create",
        "account_read",
        "account_update",
        "account_close",
        "transaction_validate",
        "loan_approve",
        "report_generate"
    ],
    "guichetier": [
        "account_create",
        "account_read",
        "transaction_create",
        "transaction_validate"
    ],
    "client": [
        "account_read",
        "transaction_read",
        "loan_request"
    ]
}

# Intégrations
INTEGRATIONS = {
    "accounting": {
        "enabled": True,
        "auto_reconcile": True
    },
    "mobile_money": {
        "enabled": False,
        "provider": ""
    }
}

# Configuration SWIFT/SEPA
INTERNATIONAL_CONFIG = {
    "swift_enabled": True,
    "sepa_enabled": False,
    "iban_required": True,
    "bic_required": True
}

# Configuration des risques
RISK_CONFIG = {
    "max_overdraft": 100000,
    "loan_to_value": 0.8,
    "debt_to_income": 0.4
}

# Performance
PERFORMANCE_CONFIG = {
    "max_transactions_per_page": 50,
    "enable_caching": True
}

# Logging
LOGGING_CONFIG = {
    "level": "INFO",
    "file": "logs/banque.log",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "audit_enabled": True
}
