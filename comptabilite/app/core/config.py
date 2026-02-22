"""
Configuration du module comptabilité

Ce module contient la configuration du projet
pour le module de comptabilité.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""

# Configuration du module comptabilite

# Paramètres de configuration
MODULE_NAME = "comptabilite"
MODULE_VERSION = "1.0.0"

# Types de comptes
ACCOUNT_TYPES = [
    "actif",
    "passif",
    "charge",
    "produit",
    "capitaux_propres"
]

# Sous-types de comptes
ACCOUNT_SUBTYPES = {
    "actif": [
        "actif_courant",
        "actif_non_courant",
        "tresorerie"
    ],
    "passif": [
        "passif_courant",
        "passif_non_courant",
        "capitaux_propres"
    ],
    "charge": [
        "charge_exploitation",
        "charge_financiere",
        "charge_exceptionnelle"
    ],
    "produit": [
        "produit_exploitation",
        "produit_financier",
        "produit_exceptionnel"
    ]
}

# Plan comptable minimum (Sénégal)
MINIMUM_CHART_OF_ACCOUNTS = [
    {"code": "401", "name": "Fournisseurs", "type": "passif_courant"},
    {"code": "411", "name": "Clients", "type": "actif_courant"},
    {"code": "501", "name": "Caisse", "type": "tresorerie"},
    {"code": "521", "name": "Banque", "type": "tresorerie"},
    {"code": "601", "name": "Achats", "type": "charge_exploitation"},
    {"code": "701", "name": "Ventes", "type": "produit_exploitation"},
    {"code": "626", "name": "Frais de transport", "type": "charge_exploitation"},
    {"code": "641", "name": "Salaires", "type": "charge_exploitation"},
    {"code": "681", "name": "Dotations aux amortissements", "type": "charge_exploitation"}
]

# Types de journaux
JOURNAL_TYPES = [
    "achat",
    "vente",
    "tresorerie",
    "general",
    "od"  # Opérations Diverse
]

# Types de documents
DOCUMENT_TYPES = [
    "facture",
    "avoir",
    "recu",
    "paiement",
    "note_frais"
]

# Modes de paiement
PAYMENT_METHODS = [
    "especes",
    "cheque",
    "virement",
    "carte_bancaire",
    "mobile_money",
    "traite"
]

# Statuts de facture
INVOICE_STATUS = [
    "brouillon",
    "soumise",
    "validee",
    "payee",
    "impayee",
    "annulee"
]

# Taux de TVA
VAT_RATES = [
    {"code": "STANDARD", "rate": 18, "name": "Taux Standard"},
    {"code": "REDUIT", "rate": 10, "name": "Taux Réduit"},
    {"code": "SUPER_REDUIT", "rate": 5, "name": "Taux Super Réduit"},
    {"code": "EXONERE", "rate": 0, "name": "Exonéré"}
]

# Configuration de la TVA
VAT_CONFIG = {
    "default_rate": 18,
    "default_inclusive": False,
    "tax_point": "invoice_date"
}

# Devises
CURRENCIES = [
    {"code": "XOF", "symbol": "XOF", "name": "Franc CFA", "decimal": 0},
    {"code": "EUR", "symbol": "€", "name": "Euro", "decimal": 2},
    {"code": "USD", "symbol": "$", "name": "Dollar US", "decimal": 2}
]

# Exercice comptable
FISCAL_YEAR_CONFIG = {
    "start_month": 1,
    "start_day": 1,
    "end_month": 12,
    "end_day": 31,
    "periods": 12
}

# Configuration de la clôture
CLOSING_CONFIG = {
    "auto_close_monthly": True,
    "auto_close_yearly": False,
    "require_approval": True,
    "backup_before_close": True
}

# Rôles et permissions
ROLE_PERMISSIONS = {
    "admin_compta": [
        "account_create",
        "account_read",
        "account_update",
        "account_delete",
        "journal_entry_create",
        "journal_entry_validate",
        "invoice_create",
        "invoice_validate",
        "payment_create",
        "report_generate",
        "fiscal_year_close"
    ],
    "comptable": [
        "account_read",
        "journal_entry_create",
        "journal_entry_validate",
        "invoice_create",
        "invoice_validate",
        "payment_create",
        "report_generate"
    ],
    "assistant_comptable": [
        "account_read",
        "journal_entry_create",
        "invoice_create",
        "payment_create"
    ]
}

# Configuration des alertes
ALERT_CONFIG = {
    "unpaid_invoice_days": 30,
    "low_balance_warning": 100000,
    "budget_overrun_percent": 10
}

# Intégrations
INTEGRATIONS = {
    "banking": {
        "enabled": True,
        "auto_reconcile": True
    },
    "inventory": {
        "enabled": True,
        "sync": "real_time"
    },
    "pos": {
        "enabled": True,
        "auto_invoice": True
    }
}

# Paramètres de reporting
REPORT_CONFIG = {
    "default_currency": "XOF",
    "show_cents": False,
    "fiscal_year_format": "YYYY",
    "include_comparison": True
}

# Configuration des exports
EXPORT_CONFIG = {
    "format": "pdf",
    "include_logo": True,
    "footer_text": "Merci de votre confiance"
}

# Performance
PERFORMANCE_CONFIG = {
    "max_entries_per_page": 50,
    "enable_caching": True,
    "query_timeout": 30
}

# Logging
LOGGING_CONFIG = {
    "level": "INFO",
    "file": "logs/comptabilite.log",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "audit_enabled": True
}
