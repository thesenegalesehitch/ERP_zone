"""
Configuration du module gestion des clients (CRM)

Ce module contient la configuration du projet
pour le module de gestion de la relation client.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""

# Configuration du module gestion_clients

# Paramètres de configuration
MODULE_NAME = "gestion_clients"
MODULE_VERSION = "1.0.0"

# Types de clients
CLIENT_TYPES = [
    "particulier",
    "entreprise",
    "administration",
    "association"
]

# Segmentations client
CLIENT_SEGMENTS = [
    "vip",
    "fidele",
    "potentiel",
    "nouveau",
    "inactif",
    "a_risque"
]

# Sources de prospection
LEAD_SOURCES = [
    "site_web",
    "recommendation",
    "salon",
    "publicite",
    "cold_call",
    "reseaux_sociaux",
    "partenariat",
    "autre"
]

# Statuts des prospects
LEAD_STATUS = [
    "nouveau",
    "contacte",
    "qualifie",
    "proposition",
    "negociation",
    "gan",
    "perdu"
]

# Statuts des clients
CLIENT_STATUS = [
    "actif",
    "inactif",
    "prospect",
    "ancien"
]

# Canaux de communication
COMMUNICATION_CHANNELS = [
    "email",
    "telephone",
    "sms",
    "whatsapp",
    "visio",
    "physique"
]

# Types de documents
DOCUMENT_TYPES = [
    "contrat",
    "devis",
    "facture",
    "bon_commande",
    "produit",
    "presentation"
]

# Configuration du scoring
SCORING_CONFIG = {
    "budget_weight": 0.30,
    "authority_weight": 0.20,
    "need_weight": 0.30,
    "timeline_weight": 0.20,
    "auto_update": True,
    "recalculate_frequency": "daily"
}

# Seuils de qualification
QUALIFICATION_THRESHOLDS = {
    "hot": 8,
    "warm": 6,
    "cold": 4
}

# Niveaux de priorité
PRIORITY_LEVELS = [
    "basse",
    "moyenne",
    "haute",
    "critique"
]

# Types d'activités
ACTIVITY_TYPES = [
    "appel",
    "email",
    "reunion",
    "tache",
    "note",
    "document",
    "contrat"
]

# Configuration des campagnes
CAMPAIGN_CONFIG = {
    "email_provider": "smtp",
    "sms_provider": "local",
    "track_opens": True,
    "track_clicks": True,
    "utm_tracking": True
}

# Types de campagnes
CAMPAIGN_TYPES = [
    "email",
    "sms",
    "telemarketing",
    "evenement",
    "webinar"
]

# Configuration du support
SUPPORT_CONFIG = {
    "ticket_system_enabled": True,
    "sla_enabled": True,
    "auto_assign": True,
    "escalation_enabled": True
}

# SLA en heures
SLA_LEVELS = {
    "critique": {
        "first_response": 1,
        "resolution": 4
    },
    "haute": {
        "first_response": 4,
        "resolution": 24
    },
    "moyenne": {
        "first_response": 24,
        "resolution": 72
    },
    "basse": {
        "first_response": 48,
        "resolution": 168
    }
}

# Catégories de tickets
TICKET_CATEGORIES = [
    "technique",
    "facturation",
    "produit",
    "autre"
]

# Rôles et permissions
ROLE_PERMISSIONS = {
    "admin_crm": [
        "client_create",
        "client_read",
        "client_update",
        "client_delete",
        "lead_manage",
        "campaign_manage",
        "report_generate",
        "settings_manage"
    ],
    "commercial": [
        "client_create",
        "client_read",
        "client_update",
        "lead_create",
        "lead_update",
        "quote_create"
    ],
    "support": [
        "ticket_create",
        "ticket_read",
        "ticket_update",
        "client_read"
    ],
    "client": [
        "profile_read",
        "ticket_create"
    ]
}

# Configuration des notifications
NOTIFICATION_CONFIG = {
    "new_lead_assign": True,
    "lead_status_change": True,
    "deal_won": True,
    "deal_lost": True,
    "ticket_assigned": True,
    "ticket_resolved": True
}

# Intégrations
INTEGRATIONS = {
    "email": {
        "enabled": True,
        "smtp_server": "smtp.example.com"
    },
    "sms": {
        "enabled": False,
        "provider": ""
    },
    "phone": {
        "enabled": False,
        "provider": ""
    },
    "calendar": {
        "enabled": False,
        "provider": "google"
    }
}

# Paramètres de confidentialité
PRIVACY_CONFIG = {
    "gdpr_compliant": True,
    "data_retention_years": 5,
    "consent_required": True,
    "right_to_erasure": True
}

# Configuration des rapports
REPORT_CONFIG = {
    "dashboard_refresh": 300,
    "charts_enabled": True,
    "export_formats": ["pdf", "excel", "csv"]
}

# Performance
PERFORMANCE_CONFIG = {
    "max_leads_per_page": 50,
    "cache_enabled": True,
    "search_enabled": True
}

# Logging
LOGGING_CONFIG = {
    "level": "INFO",
    "file": "logs/gestion_clients.log",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
}
