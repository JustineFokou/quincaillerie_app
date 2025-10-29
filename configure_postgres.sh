#!/bin/bash

# Configuration PostgreSQL pour l'application Quincaillerie
echo "🐘 Configuration PostgreSQL pour Quincaillerie"
echo "=============================================="

# Vérifier si nous pouvons nous connecter en tant que postgres
echo "🔍 Test de connexion..."

# Essayer de créer l'utilisateur et la base de données
echo "👤 Création de l'utilisateur et de la base de données..."

# Utiliser sudo pour exécuter les commandes PostgreSQL
sudo -u postgres psql << 'EOF'
-- Vérifier si l'utilisateur existe déjà
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'quincaillerie_user') THEN
        CREATE USER quincaillerie_user WITH PASSWORD 'quincaillerie_password';
        RAISE NOTICE 'Utilisateur quincaillerie_user créé';
    ELSE
        RAISE NOTICE 'Utilisateur quincaillerie_user existe déjà';
    END IF;
END
$$;

-- Vérifier si la base de données existe déjà
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'quincaillerie_db') THEN
        CREATE DATABASE quincaillerie_db OWNER quincaillerie_user;
        RAISE NOTICE 'Base de données quincaillerie_db créée';
    ELSE
        RAISE NOTICE 'Base de données quincaillerie_db existe déjà';
    END IF;
END
$$;

-- Donner tous les privilèges
GRANT ALL PRIVILEGES ON DATABASE quincaillerie_db TO quincaillerie_user;

-- Se connecter à la base de données et configurer les privilèges
\c quincaillerie_db;
GRANT ALL ON SCHEMA public TO quincaillerie_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO quincaillerie_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO quincaillerie_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO quincaillerie_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO quincaillerie_user;

\q
EOF

if [ $? -eq 0 ]; then
    echo "✅ Configuration PostgreSQL réussie !"
    echo ""
    echo "📋 Informations de connexion :"
    echo "   - Host: localhost"
    echo "   - Port: 5432"
    echo "   - Database: quincaillerie_db"
    echo "   - User: quincaillerie_user"
    echo "   - Password: quincaillerie_password"
    echo ""
    
    # Tester la connexion
    echo "🔍 Test de connexion..."
    if PGPASSWORD=quincaillerie_password psql -h localhost -U quincaillerie_user -d quincaillerie_db -c "SELECT 'Connexion réussie' as status;" 2>/dev/null; then
        echo "✅ Connexion testée avec succès !"
        
        # Mettre à jour le fichier .env
        echo "🔧 Mise à jour du fichier .env..."
        cat > .env << 'EOF'
DEBUG=True
SECRET_KEY=django-insecure-2(6b!ou)efk6*-bz3p7hr50(fw44sc%)@&z^rf+_u**n)#2cb7
DATABASE_URL=postgresql://quincaillerie_user:quincaillerie_password@localhost:5432/quincaillerie_db
ALLOWED_HOSTS=localhost,127.0.0.1
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
EOF
        echo "✅ Fichier .env mis à jour"
        
    else
        echo "❌ Test de connexion échoué"
    fi
    
else
    echo "❌ Erreur lors de la configuration PostgreSQL"
fi

