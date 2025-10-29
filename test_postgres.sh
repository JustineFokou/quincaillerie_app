#!/bin/bash

# Test de connexion PostgreSQL
echo "🔍 Test de connexion PostgreSQL..."

# Essayer différentes méthodes de connexion
echo "1. Test avec utilisateur système..."
if psql -d postgres -c "SELECT 1;" 2>/dev/null; then
    echo "✅ Connexion réussie avec utilisateur système"
    USER_METHOD="system"
else
    echo "❌ Connexion échouée avec utilisateur système"
fi

echo "2. Test avec utilisateur postgres..."
if psql -U postgres -d postgres -c "SELECT 1;" 2>/dev/null; then
    echo "✅ Connexion réussie avec utilisateur postgres"
    USER_METHOD="postgres"
else
    echo "❌ Connexion échouée avec utilisateur postgres"
fi

echo "3. Test avec utilisateur $USER..."
if psql -U $USER -d postgres -c "SELECT 1;" 2>/dev/null; then
    echo "✅ Connexion réussie avec utilisateur $USER"
    USER_METHOD="$USER"
else
    echo "❌ Connexion échouée avec utilisateur $USER"
fi

# Afficher les informations sur PostgreSQL
echo ""
echo "📊 Informations PostgreSQL :"
echo "Version: $(psql --version)"
echo "Utilisateur actuel: $USER"
echo "Host: $(hostname)"

# Vérifier les processus PostgreSQL
echo ""
echo "🔄 Processus PostgreSQL :"
ps aux | grep postgres | grep -v grep || echo "Aucun processus PostgreSQL trouvé"

# Vérifier les ports
echo ""
echo "🌐 Ports PostgreSQL :"
netstat -tlnp | grep 5432 || echo "Port 5432 non ouvert"
