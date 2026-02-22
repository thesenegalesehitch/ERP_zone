"""
Configuration du module gestion des approvisionnements

Ce module contient la configuration du Projet
pour le module de gestion des approvisionnements et achats.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""

# Configuration du module gestion_approvisionnement

# Paramètres de configuration
MODULE_NAME = "gestion_approvisionnement"
MODULE_VERSION = "1.0.0"

# Types de fournisseurs
SUPPLIER_TYPES = [
    "fabricant",
    "distributeur",
    "grossiste",
    "importateur"
]

# Statuts de fournisseur
SUPPLIER_STATUS = [
    "actif",
    "inactif",
    "bloque"
]

# Statuts de commande
ORDER_STATUS = [
    "brouillon",
    "soumise",
    "approuvee",
    "envoyee",
    "recue",
    "facturee",
    "payee",
    "annulee",
    "rejetee"
]

# Types de commande
ORDER_TYPES = [
    "standard",
    "urgente",
    "planifiee"
]

# Priorités
PRIORITY_LEVELS = [
    "basse",
    "normale",
    "haute",
    "urgente"
]

# Types de réception
RECEPTION_STATUS = [
    "en_attente",
    "partielle",
    "complete",
    "annulee"
]

# Conditions de paiement
PAYMENT_TERMS = [
    {"code": "COMPTANT", "days": 0, "name": "Comptant"},
    {"code": "NET30", "days": 30, "name": "Net 30 jours"},
    {"code": "NET60", "days": 60, "name": "Net 60 jours"},
    {"code": "NET90", "days": 90, "name": "Net 90 jours"}
]

# Types de documents
DOCUMENT_TYPES = [
    "bon_commande",
    "bon_livraison",
    "facture",
    "avoir",
    "contrat"
]

# Raisons de retour
RETURN_REASONS = [
    "defectueux",
    "erreur_livraison",
    "non_conforme",
    "perime"
]

# Seuils d'alerte
ALERT_CONFIG = {
    "low_stock_warning": 10,
    "delivery_delay_days": 7,
    "payment_due_days": 30
}

# Configuration des devises
CURRENCY_CONFIG = {
    "default": "XOF",
    "supported": ["XOF", "EUR", "USD"]
}

# Rôles et permissions
ROLE_PERMISSIONS = {
    "admin_achat": [
        "supplier_manage",
        "order_create",
        "order_approve",
        "order_receive",
        "report_generate"
    ],
    "acheteur": [
        "supplier_read",
        "order_create",
        "order_update"
    ],
    "receveur": [
        "order_receive",
        "quality_check"
    ]
}

# Intégrations
INTEGRATIONS = {
    "inventory": {
        "enabled": True,
        "auto_update": True
    },
    "accounting": {
        "enabled": True
    }
}

# Performance
PERFORMANCE_CONFIG = {
    "max_orders_per_page": 50
}

# Logging
LOGGING_CONFIG = {
    "level": "INFO",
    "file": "logs/gestion_approvisionnement.log",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
}
