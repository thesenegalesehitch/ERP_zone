# =============================================================================
# Dockerfile pour le module de Gestion de Projets ERP Zone
# =============================================================================
# Ce fichier définit l'image Docker pour l'API du module de gestion de projets.
#
# Usage:
#   docker build -t erp-zone-projects .
#   docker run -p 8001:8000 erp-zone-projects
# =============================================================================

# Image de base Python 3.11
FROM python:3.11-slim

# Définition des variables d'environnement
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Mise à jour et installation des dépendances système
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Création du répertoire de travail
WORKDIR /app

# Copie des fichiers de requirements
COPY requirements.txt .

# Installation des dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code source
COPY . .

# Création de l'utilisateur non-root pour la sécurité
RUN useradd --create-home --shell /bin/bash appuser && \
    chown -R appuser:appuser /app
USER appuser

# Exposition du port
EXPOSE 8000

# Commande de démarrage
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# Labels pour les métadonnées
LABEL maintainer="ERP Zone Team" \
      version="1.0.0" \
      description="Module de gestion de projets ERP Zone" \
      documentation="https://erp-zone.docs.example.com/projects"
