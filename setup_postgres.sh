#!/bin/bash

# Script de configuration PostgreSQL pour l'application Quincaillerie
# Usage: ./setup_postgres.sh

echo "🐘 Configuration de PostgreSQL pour l'application Quincaillerie"
echo "=============================================================="

# Vérifier si PostgreSQL est installé
if ! command -v psql &> /dev/null; then
    echo "❌ PostgreSQL n'est pas installé. Installation..."
    sudo apt update
    sudo apt install -y postgresql postgresql-contrib
fi

# Vérifier si PostgreSQL est en cours d'exécution
if ! pg_isready -q; then
    echo "🔄 Démarrage de PostgreSQL..."
    sudo systemctl start postgresql
    sudo systemctl enable postgresql
fi

# Créer l'utilisateur et la base de données
echo "👤 Création de l'utilisateur et de la base de données..."

# Se connecter en tant que postgres et créer l'utilisateur
sudo -u postgres psql << EOF
-- Créer l'utilisateur
CREATE USER quincaillerie_user WITH PASSWORD 'quincaillerie_password';

-- Créer la base de données
CREATE DATABASE quincaillerie_db OWNER quincaillerie_user;

-- Donner tous les privilèges
GRANT ALL PRIVILEGES ON DATABASE quincaillerie_db TO quincaillerie_user;

-- Se connecter à la base de données et donner les privilèges sur le schéma public
\c quincaillerie_db;
GRANT ALL ON SCHEMA public TO quincaillerie_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO quincaillerie_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO quincaillerie_user;

-- Configurer les privilèges par défaut pour les futures tables
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO quincaillerie_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO quincaillerie_user;

\q
EOF

if [ $? -eq 0 ]; then
    echo "✅ Base de données PostgreSQL créée avec succès !"
    echo ""
    echo "📋 Informations de connexion :"
    echo "   - Host: localhost"
    echo "   - Port: 5432"
    echo "   - Database: quincaillerie_db"
    echo "   - User: quincaillerie_user"
    echo "   - Password: quincaillerie_password"
    echo ""
    echo "🔧 Configuration Django mise à jour automatiquement"
    
    # Mettre à jour le fichier .env
    cat > .env << EOF
DEBUG=True
SECRET_KEY=django-insecure-2(6b!ou)efk6*-bz3p7hr50(fw44sc%)@&z^rf+_u**n)#2cb7
DATABASE_URL=postgresql://quincaillerie_user:quincaillerie_password@localhost:5432/quincaillerie_db
ALLOWED_HOSTS=localhost,127.0.0.1
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
EOF
    
    echo "✅ Fichier .env mis à jour"
    echo ""
    echo "🚀 Prochaines étapes :"
    echo "   1. Activer l'environnement virtuel : source venv/bin/activate"
    echo "   2. Appliquer les migrations : python manage.py migrate"
    echo "   3. Créer un superutilisateur : python manage.py createsuperuser"
    echo "   4. Démarrer le serveur : python manage.py runserver"
    
else
    echo "❌ Erreur lors de la création de la base de données"
    echo "💡 Essayez de lancer le script avec sudo : sudo ./setup_postgres.sh"
fi
