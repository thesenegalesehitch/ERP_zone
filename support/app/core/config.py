"""
Configuration du module support

Ce module contient la configuration du Projet
pour le module de support client.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""

# Configuration du module support

# Paramètres de configuration
MODULE_NAME = "support"
MODULE_VERSION = "1.0.0"

# Types de tickets
TICKET_TYPES = [
    "incident",
    "demande",
    "question",
    "suggestion",
    "reclamation"
]

# Statuts de ticket
TICKET_STATUS = [
    "nouveau",
    "en_attente",
    "en_cours",
    "en_revision",
    "resolu",
    "ferme",
    "duplique"
]

# Priorités
PRIORITY_LEVELS = [
    "basse",
    "moyenne",
    "haute",
    "critique"
]

# Impacts
IMPACT_LEVELS = [
    "faible",
    "moyen",
    "eleve",
    "critique"
]

# Catégories de tickets
CATEGORIES = [
    "technique",
    "facturation",
    "produit",
    "service",
    "autre"
]

# Sources
SOURCES = [
    "email",
    "telephone",
    "chat",
    "reseaux_sociaux",
    "portail_client"
]

# Configuration SLA (en heures)
SLA_CONFIG = {
    "critique": {
        "first_response": 1,
        "resolution": 4,
        "escalation": 2
    },
    "haute": {
        "first_response": 4,
        "resolution": 24,
        "escalation": 12
    },
    "moyenne": {
        "first_response": 24,
        "resolution": 72,
        "escalation": 48
    },
    "basse": {
        "first_response": 48,
        "resolution": 168,
        "escalation": 120
    }
}

# Canaux de réponse
RESPONSE_CHANNELS = [
    "email",
    "telephone",
    "chat",
    "sms"
]

# Rôles et permissions
ROLE_PERMISSIONS = {
    "admin_support": [
        "ticket_create",
        "ticket_read",
        "ticket_update",
        "ticket_delete",
        "ticket_assign",
        "sla_manage",
        "report_generate",
        "kb_manage"
    ],
    "agent_support": [
        "ticket_create",
        "ticket_read",
        "ticket_update",
        "ticket_assign",
        "kb_read"
    ],
    "client": [
        "ticket_create",
        "ticket_read",
        "ticket_comment"
    ]
}

# Configuration des emails
EMAIL_CONFIG = {
    "auto_response": True,
    "attach_ticket": True,
    "notify_updates": True
}

# Intégrations
INTEGRATIONS = {
    "crm": {
        "enabled": True,
        "module": "gestion_clients"
    },
    "knowledge_base": {
        "enabled": True,
        "auto_suggest": True
    },
    "chat": {
        "enabled": False
    }
}

# Configuration des escalades
ESCALATION_CONFIG = {
    "enabled": True,
    "auto_escalate": True,
    "notify_manager": True
}

# Performance
PERFORMANCE_CONFIG = {
    "max_tickets_per_page": 50,
    "enable_caching": True
}

# Logging
LOGGING_CONFIG = {
    "level": "INFO",
    "file": "logs/support.log",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
}
