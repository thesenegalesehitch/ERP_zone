"""
Configuration du module restaurant

Ce module contient la configuration du Projet
pour le module de gestion de restaurant.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""

# Configuration du module restaurant

# Paramètres de configuration
MODULE_NAME = "restaurant"
MODULE_VERSION = "1.0.0"

# Types de service
SERVICE_TYPES = [
    "petit_dejeuner",
    "dejeuner",
    "diner",
    "snack",
    "bar"
]

# Statuts de commande
ORDER_STATUS = [
    "en_attente",
    "confirmee",
    "en_preparation",
    "prete",
    "servie",
    "payee",
    "annulee"
]

# Types de commande
ORDER_TYPES = [
    "sur_place",
    "a_emporter",
    "livraison"
]

# Statuts de table
TABLE_STATUS = [
    "disponible",
    "reservee",
    "occupyee",
    "nettoyage"
]

# Types de paiement
PAYMENT_METHODS = [
    "especes",
    "carte",
    "mobile_money",
    "cheque",
    "ticket_restaurant"
]

# Catégories de menu
MENU_CATEGORIES = [
    "entree",
    "plat_principal",
    "dessert",
    "boisson",
    "accompagnement"
]

# Statuts de paiement
PAYMENT_STATUS = [
    "en_attente",
    "partiel",
    "paye",
    "rembourse"
]

# Configuration des réservations
RESERVATION_CONFIG = {
    "max_party_size": 20,
    "default_duration_minutes": 90,
    "advance_booking_days": 30,
    "min_advance_hours": 2
}

# Heures d'ouverture
OPENING_HOURS = {
    "petit_dejeuner": {"start": "06:00", "end": "10:00"},
    "dejeuner": {"start": "12:00", "end": "15:00"},
    "diner": {"start": "19:00", "end": "23:00"},
    "snack": {"start": "10:00", "end": "22:00"}
}

# Rôles et permissions
ROLE_PERMISSIONS = {
    "admin_restaurant": [
        "menu_manage",
        "table_manage",
        "order_manage",
        "report_generate"
    ],
    "serveur": [
        "order_create",
        "order_update",
        "table_status"
    ],
    "cuisinier": [
        "kitchen_view",
        "order_prepare"
    ],
    "caissier": [
        "payment_process",
        "receipt_print"
    ]
}

# Intégrations
INTEGRATIONS = {
    "inventory": {
        "enabled": True,
        "auto_deduct": True
    },
    "accounting": {
        "enabled": True
    }
}

# Configuration de la cuisine
KITCHEN_CONFIG = {
    "ticket_printer": True,
    "auto_assign": True,
    "timeout_minutes": 30
}

# Performance
PERFORMANCE_CONFIG = {
    "max_orders_per_page": 50
}

# Logging
LOGGING_CONFIG = {
    "level": "INFO",
    "file": "logs/restaurant.log",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
}
