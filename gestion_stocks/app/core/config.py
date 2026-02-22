"""
Configuration du module gestion des stocks

Ce module contient la configuration du projet
pour le module de gestion des stocks.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""

# Configuration du module gestion_stocks

# Paramètres de configuration
MODULE_NAME = "gestion_stocks"
MODULE_VERSION = "1.0.0"

# Configuration de la base de données
DATABASE_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "name": "erp_gestion_stocks",
    "pool_size": 10,
    "max_overflow": 20
}

# Configuration du cache
CACHE_CONFIG = {
    "enabled": True,
    "ttl": 300,
    "prefix": "gs_"
}

# Types d'articles
ARTICLE_TYPES = [
    "produit_fini",
    "matiere_premiere",
    "composant",
    "emballage",
    "consommable"
]

# Unités de mesure
UNITS_OF_MEASURE = [
    {"code": "UN", "name": "Unité", "type": "count"},
    {"code": "KG", "name": "Kilogramme", "type": "weight"},
    {"code": "L", "name": "Litre", "type": "volume"},
    {"code": "M", "name": "Mètre", "type": "length"},
    {"code": "M2", "name": "Mètre carré", "type": "area"},
    {"code": "M3", "name": "Mètre cube", "type": "volume"},
    {"code": "BOX", "name": "Boîte", "type": "count"},
    {"code": "PAL", "name": "Palette", "type": "count"}
]

# Méthodes d'évaluation des stocks
VALUATION_METHODS = [
    "fifo",  # First In, First Out
    "lifo",  # Last In, First Out
    "average",  # Coût moyen
    "specific"  # Coût spécifique
]

# Niveaux d'alerte
ALERT_LEVELS = {
    "critical": {
        "threshold_percent": 10,
        "notify": ["admin", "gestionnaire_stocks"],
        "color": "red"
    },
    "warning": {
        "threshold_percent": 25,
        "notify": ["gestionnaire_stocks"],
        "color": "orange"
    },
    "info": {
        "threshold_percent": 50,
        "notify": [],
        "color": "yellow"
    }
}

# Configuration des entrepôts
WAREHOUSE_CONFIG = {
    "default_location": "principal",
    "enable_multi_warehouse": True,
    "transfer_enabled": True,
    "default_valuation": "average"
}

# Types de mouvements de stock
MOVEMENT_TYPES = [
    "entree",
    "sortie",
    "transfert",
    "ajustement_positif",
    "ajustement_negatif",
    "retour",
    "destruction"
]

# Raisons d'ajustement
ADJUSTMENT_REASONS = [
    "erreur_saisie",
    "dommage",
    "perte",
    "vol",
    "inventaire",
    "autre"
]

# Configuration descodes-barres
BARCODE_CONFIG = {
    "format": "EAN13",
    "prefix": "200",
    "generate_checksum": True
}

# Paramètres de commande
ORDER_CONFIG = {
    "reorder_point_default": 10,
    "safety_stock_default": 5,
    "lead_time_default_days": 7,
    "eoq_enabled": True
}

# Configuration des alertes
ALERT_CONFIG = {
    "low_stock_enabled": True,
    "expiry_warning_days": 30,
    "overstock_warning_percent": 150,
    "email_notifications": True
}

# Paramètres d'inventaire
INVENTORY_CONFIG = {
    "full_inventory_frequency": "annuel",
    "cycle_count_enabled": True,
    "abc_analysis_enabled": True,
    "valuation_on_inventory": True
}

# Configuration de la traçabilité
TRACEABILITY_CONFIG = {
    "enabled": True,
    "track_lot": True,
    "track_expiry": True,
    "track_origin": True,
    "retention_days": 365
}

# Configuration des imports/exports
IMPORT_EXPORT_CONFIG = {
    "csv_delimiter": ";",
    "csv_encoding": "utf-8",
    "excel_enabled": True,
    "max_rows": 10000
}

# Intégrations
INTEGRATIONS = {
    "ecommerce": {
        "enabled": False,
        "platform": "magento"
    },
    "accounting": {
        "enabled": True,
        "module": "comptabilite"
    },
    "pos": {
        "enabled": True,
        "module": "point_vente"
    }
}

# Performance
PERFORMANCE_CONFIG = {
    "max_results": 100,
    "enable_compression": True,
    "cache_queries": True
}

# Logging
LOGGING_CONFIG = {
    "level": "INFO",
    "file": "logs/gestion_stocks.log",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
}
