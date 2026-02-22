"""
Configuration du module production

Ce module contient la configuration du Projet
pour le module de gestion de la production.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""

# Configuration du module production

# Paramètres de configuration
MODULE_NAME = "production"
MODULE_VERSION = "1.0.0"

# Types de production
PRODUCTION_TYPES = [
    "serie",
    "unitaire",
    "continue",
    "par_lot"
]

# Statuts de production
PRODUCTION_STATUS = [
    "planifie",
    "en_cours",
    "en_pause",
    "termine",
    "annule"
]

# Types d'ordres de fabrication
WORK_ORDER_TYPES = [
    "fabrication",
    "assemblage",
    "reparation",
    "maintenance"
]

# Statuts des ordres de travail
WORK_ORDER_STATUS = [
    "planifie",
    "lance",
    "en_cours",
    "termine",
    "annule"
]

# Niveaux de priorité
PRIORITY_LEVELS = [
    "basse",
    "normale",
    "haute",
    "urgente"
]

# Types de postes de travail
WORKSTATION_TYPES = [
    "machine",
    "poste_manuel",
    "poste_assemblage",
    "poste_controle"
]

# Statuts des postes
WORKSTATION_STATUS = [
    "disponible",
    "en_production",
    "maintenance",
    "hors_service"
]

# Types de maintenance
MAINTENANCE_TYPES = [
    "preventive",
    "corrective",
    "predictive",
    "conditionnelle"
]

# Types de qualité
QUALITY_CHECK_TYPES = [
    "avant_production",
    "pendant_production",
    "apres_production",
    "finale"
]

# Résultats de contrôle
QUALITY_RESULTS = [
    "conforme",
    "non_conforme",
    "rebut",
    "rework"
]

# Configuration de la planification
PLANNING_CONFIG = {
    "horizon_jours": 30,
    "planification_auto": True,
    "considerer_stocks": True
}

# Gammes de fabrication
ROUTING_TYPES = [
    "standard",
    "alternative",
    "emergency"
]

# Unités de mesure temps
TIME_UNITS = [
    "minutes",
    "heures",
    "jours"
]

# Rôles et permissions
ROLE_PERMISSIONS = {
    "admin_prod": [
        "production_create",
        "production_read",
        "production_update",
        "production_delete",
        "workstation_manage",
        "quality_manage",
        "report_generate"
    ],
    "chef_production": [
        "production_create",
        "production_read",
        "production_update",
        "work_order_create",
        "quality_check"
    ],
    "operateur": [
        "production_read",
        "work_order_update",
        "quality_record"
    ]
}

# Configuration des seuils
THRESHOLD_CONFIG = {
    "defect_rate_warning": 5,
    "defect_rate_critical": 10,
    "utilization_min": 70,
    "oee_target": 85
}

# Calcul OEE
OEE_WEIGHTS = {
    "availability": 0.333,
    "performance": 0.333,
    "quality": 0.334
}

# Intégrations
INTEGRATIONS = {
    "inventory": {
        "enabled": True,
        "auto_reserve": True
    },
    "accounting": {
        "enabled": True,
        "cost_tracking": True
    },
    "maintenance": {
        "enabled": True,
        "predictive": False
    }
}

# Configuration de la qualité
QUALITY_CONFIG = {
    "sampling_rate": 10,  # Pourcentage
    "auto_approve": False,
    "traceability": True
}

# Performance
PERFORMANCE_CONFIG = {
    "max_orders_per_page": 50,
    "enable_caching": True
}

# Logging
LOGGING_CONFIG = {
    "level": "INFO",
    "file": "logs/production.log",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
}
