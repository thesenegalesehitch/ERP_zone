"""
Configuration du module point de vente

Ce module contient la configuration du Projet
pour le module de point de vente (POS).

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""

# Configuration du module point_vente

# Paramètres de configuration
MODULE_NAME = "point_vente"
MODULE_VERSION = "1.0.0"

# Types de vente
SALE_TYPES = [
    " comptoir",
    "sur_place",
    "livraison",
    "en_ligne"
]

# Statuts de vente
SALE_STATUS = [
    "en_cours",
    "terminee",
    "annulee",
    "remboursement"
]

# Modes de paiement
PAYMENT_METHODS = [
    "especes",
    "carte_bancaire",
    "carte_credit",
    "mobile_money",
    "cheque",
    "virement"
]

# Types de remise
DISCOUNT_TYPES = [
    "percent",
    "fixed",
    "loyalty"
]

# Statuts de paiement
PAYMENT_STATUS = [
    "en_attente",
    "partiel",
    "paye",
    "echoue",
    "rembourse"
]

# Statuts de table
TABLE_STATUS = [
    "disponible",
    "reservee",
    "occupyee",
    "nettoyage"
]

# Types de client
CLIENT_TYPES = [
    "occasionnel",
    "fidele",
    "grossiste",
    "vip"
]

# Configuration des reçus
RECEIPT_CONFIG = {
    "show_logo": True,
    "show_barcode": True,
    "show_qr_code": False,
    "footer_text": "Merci de votre visite!"
}

# Configuration des taxes
TAX_CONFIG = {
    "default_rate": 18,
    "included_in_price": False
}

# Rôles et permissions
ROLE_PERMISSIONS = {
    "admin_pos": [
        "sale_create",
        "sale_read",
        "sale_update",
        "sale_delete",
        "refund_approve",
        "report_generate",
        "settings_manage"
    ],
    "caissier": [
        "sale_create",
        "sale_read",
        "payment_process"
    ],
    "manager": [
        "sale_create",
        "sale_read",
        "discount_apply",
        "refund_create",
        "report_view"
    ]
}

# Intégrations
INTEGRATIONS = {
    "inventory": {
        "enabled": True,
        "auto_update": True
    },
    "accounting": {
        "enabled": True,
        "auto_invoice": True
    },
    "loyalty": {
        "enabled": True,
        "points_rate": 1  # 1 XOF = 1 point
    }
}

# Configuration du clavier tactile
TOUCH_KEYBOARD_CONFIG = {
    "rows": 4,
    "columns": 5,
    "quick_buttons": 20
}

# Performance
PERFORMANCE_CONFIG = {
    "max_items_per_sale": 100,
    "receipt_printer": True,
    "auto_logout_minutes": 15
}

# Logging
LOGGING_CONFIG = {
    "level": "INFO",
    "file": "logs/point_vente.log",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
}
