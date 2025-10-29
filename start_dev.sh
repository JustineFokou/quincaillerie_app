#!/bin/bash

# Script de démarrage pour l'application Quincaillerie
# Usage: ./start_dev.sh

echo "🚀 Démarrage de l'application Quincaillerie"
echo "=========================================="

# Vérifier si l'environnement virtuel existe
if [ ! -d "venv" ]; then
    echo "❌ Environnement virtuel non trouvé. Création..."
    python3 -m venv venv
fi

# Activer l'environnement virtuel
echo "📦 Activation de l'environnement virtuel..."
source venv/bin/activate

# Installer les dépendances si nécessaire
if [ ! -f "venv/pyvenv.cfg" ] || [ ! -d "venv/lib/python3.10/site-packages/django" ]; then
    echo "📥 Installation des dépendances..."
    pip install -r requirements.txt
fi

# Appliquer les migrations
echo "🗄️ Application des migrations..."
python manage.py migrate

# Collecter les fichiers statiques
echo "📁 Collecte des fichiers statiques..."
python manage.py collectstatic --noinput

# Créer un superutilisateur si nécessaire
if [ ! -f "superuser_created" ]; then
    echo "👤 Création du superutilisateur..."
    echo "from utilisateurs.models import User; User.objects.create_superuser('admin', 'admin@quincaillerie.com', 'admin123', role='ADMIN')" | python manage.py shell
    touch superuser_created
fi

# Créer des données de test si nécessaire
if [ ! -f "test_data_created" ]; then
    echo "🧪 Création des données de test..."
    python manage.py shell -c "
from produits.models import Categorie, Produit
from fournisseurs.models import Fournisseur
from stocks.models import MouvementStock
from django.utils import timezone

# Créer des catégories
cat1 = Categorie.objects.create(nom='Outillage', description='Outils de bricolage', couleur='#3B82F6')
cat2 = Categorie.objects.create(nom='Quincaillerie', description='Articles de quincaillerie', couleur='#10B981')

# Créer des fournisseurs
four1 = Fournisseur.objects.create(
    nom='Outils Pro', 
    contact='Jean Dupont', 
    email='contact@outilspro.fr', 
    telephone='01 23 45 67 89',
    adresse='123 Rue des Outils',
    ville='Paris',
    code_postal='75001'
)

# Créer des produits
prod1 = Produit.objects.create(
    code_produit='OUT001',
    nom='Marteau 500g',
    description='Marteau de menuisier 500g avec manche en bois',
    categorie=cat1,
    prix_achat=15.50,
    prix_vente=25.00,
    seuil_alerte=5,
    fournisseur_principal=four1
)

# Créer des mouvements de stock
MouvementStock.objects.create(
    produit=prod1,
    type_mouvement='ENTREE',
    quantite=20,
    motif='ACHAT',
    reference='FAC001',
    prix_unitaire=15.50,
    fournisseur=four1,
    date_mouvement=timezone.now()
)

print('Données de test créées avec succès !')
"
    touch test_data_created
fi

echo ""
echo "✅ Application prête !"
echo ""
echo "🌐 Accès à l'application :"
echo "   - Interface web : http://localhost:8000"
echo "   - Administration : http://localhost:8000/admin"
echo ""
echo "🔐 Compte de test :"
echo "   - Utilisateur : admin"
echo "   - Mot de passe : admin123"
echo ""
echo "🚀 Démarrage du serveur de développement..."
echo "   Appuyez sur Ctrl+C pour arrêter"
echo ""

# Démarrer le serveur Django
python manage.py runserver 0.0.0.0:8000
