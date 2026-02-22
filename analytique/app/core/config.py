"""
Configuration du module analytique

Ce module contient la configuration du Projet
pour le module analytique et rapports.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""

# Configuration du module analytique

# Paramètres de configuration
MODULE_NAME = "analytique"
MODULE_VERSION = "1.0.0"

# Types de rapports
REPORT_TYPES = [
    "vente",
    "achat",
    "stock",
    "financier",
    "rh",
    "production",
    "projet"
]

# Formats d'export
EXPORT_FORMATS = [
    "pdf",
    "excel",
    "csv",
    "json"
]

# Types de graphiques
CHART_TYPES = [
    "bar",
    "line",
    "pie",
    "area",
    "scatter"
]

# Périodes de rapport
REPORT_PERIODS = [
    "journalier",
    "hebdomadaire",
    "mensuel",
    "trimestriel",
    "annuel",
    "personnalise"
]

# Indicateurs de performance (KPI)
KPI_CATEGORIES = [
    "vente",
    "achat",
    "production",
    "rh",
    "financier"
]

# Types de tableaux de bord
DASHBOARD_TYPES = [
    "commercial",
    "production",
    "financier",
    "rh",
    "personnalise"
]

# Rôles et permissions
ROLE_PERMISSIONS = {
    "admin_analytique": [
        "report_create",
        "report_read",
        "report_export",
        "dashboard_manage",
        "kpi_manage"
    ],
    "manager": [
        "report_read",
        "report_export",
        "dashboard_view"
    ],
    "employee": [
        "dashboard_view"
    ]
}

# Configuration du cache
CACHE_CONFIG = {
    "enabled": True,
    "ttl": 300
}

# Configuration de l'export
EXPORT_CONFIG = {
    "max_rows": 100000,
    "compression": True
}

# Intégrations
INTEGRATIONS = {
    "all_modules": {
        "enabled": True
    }
}

# Performance
PERFORMANCE_CONFIG = {
    "max_results": 1000,
    "timeout": 30
}

# Logging
LOGGING_CONFIG = {
    "level": "INFO",
    "file": "logs/analytique.log",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
}
