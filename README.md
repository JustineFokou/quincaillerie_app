# Application de Gestion de Quincaillerie

Une application web moderne de gestion de quincaillerie développée avec Django, Tailwind CSS et Flowbite.

## 🚀 Fonctionnalités

### ✅ Fonctionnalités Implémentées

- **Dashboard** : Vue d'ensemble avec statistiques et alertes de stock
- **Gestion des Produits** : CRUD complet avec catégories et images
- **Gestion du Stock** : Suivi des mouvements d'entrée/sortie
- **Gestion des Ventes** : Création et suivi des ventes
- **Gestion des Fournisseurs** : Base de données des fournisseurs
- **Gestion des Utilisateurs** : Système de rôles (Admin, Gérant, Vendeur, Stockiste)
- **Configuration de l'Entreprise** : Enregistrement des informations de l'entreprise (nom, adresse, contacts, logo)
- **Interface d'Administration** : Interface Django Admin complète
- **Authentification** : Système de connexion/déconnexion
- **Interface Moderne** : Design responsive avec Tailwind CSS et Flowbite

### 🔄 Fonctionnalités en Cours de Développement

- **Tâches Asynchrones** : Configuration Celery pour les alertes automatiques
- **Rapports** : Génération de rapports de vente et de stock
- **Notifications** : Système d'alertes en temps réel
- **API REST** : Endpoints pour intégration mobile

## 🛠️ Technologies Utilisées

- **Backend** : Django 5.2.7 (Python 3.10)
- **Frontend** : HTML5, Tailwind CSS, Flowbite
- **Base de données** : SQLite (développement) / PostgreSQL (production)
- **Tâches asynchrones** : Celery + Redis
- **Authentification** : Django Auth avec modèle utilisateur personnalisé
- **Interface d'administration** : Django Admin

## 📦 Installation

### Prérequis

- Python 3.10+
- pip
- Redis (pour Celery)

### Installation

1. **Cloner le projet**
   ```bash
   git clone <repository-url>
   cd quincaillerie_app
   ```

2. **Créer l'environnement virtuel**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # ou
   venv\Scripts\activate     # Windows
   ```

3. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurer la base de données**
   ```bash
   python manage.py migrate
   ```

5. **Créer un superutilisateur**
   ```bash
   python manage.py createsuperuser
   ```

6. **Démarrer le serveur**
   ```bash
   python manage.py runserver
   ```

## 🔐 Comptes de Test

Un compte administrateur est créé automatiquement :
- **Utilisateur** : `admin`
- **Mot de passe** : `admin123`

## 📁 Structure du Projet

```
quincaillerie_app/
├── core/                    # Application principale (dashboard)
├── produits/               # Gestion des produits et catégories
├── stocks/                 # Gestion des mouvements de stock
├── ventes/                 # Gestion des ventes
├── fournisseurs/           # Gestion des fournisseurs
├── utilisateurs/           # Gestion des utilisateurs et authentification
├── quincaillerie/          # Configuration Django
├── templates/              # Templates HTML
├── static/                 # Fichiers statiques
└── media/                  # Fichiers uploadés
```

## 🎯 Modèles de Données

### Produits
- Code produit unique
- Nom, description, catégorie
- Prix d'achat et de vente
- Seuil d'alerte de stock
- Image et fournisseur principal

### Stock
- Mouvements d'entrée/sortie
- Suivi des quantités
- Historique des mouvements
- Calcul automatique du stock actuel

### Ventes
- Numéro de vente unique
- Informations client
- Lignes de vente détaillées
- Calcul automatique des totaux

### Utilisateurs
- Rôles personnalisés (Admin, Gérant, Vendeur, Stockiste)
- Permissions granulaires
- Profils utilisateur étendus

### Configuration de l'Entreprise
- Informations de l'entreprise (nom, slogan, adresse)
- Contacts (téléphones, email, site web)
- Logo de l'entreprise
- Numéro fiscal
- Devise par défaut
- Interface d'administration dédiée

## 🚀 Déploiement

### Variables d'environnement

Créer un fichier `.env` :
```env
DEBUG=False
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:password@localhost:5432/quincaillerie
ALLOWED_HOSTS=yourdomain.com
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

### Production avec Render

1. Connecter le repository GitHub
2. Configurer les variables d'environnement
3. Déployer automatiquement

## 📊 Fonctionnalités du Dashboard

- **Statistiques générales** : Nombre de produits, catégories, fournisseurs
- **Alertes de stock** : Produits en rupture de stock
- **Ventes récentes** : Dernières transactions
- **Actions rapides** : Accès direct aux fonctions principales
- **Chiffre d'affaires** : CA du mois en cours

## 🔧 Configuration Celery

Pour les tâches asynchrones (alertes automatiques) :

```bash
# Démarrer Redis
redis-server

# Démarrer Celery Worker
celery -A quincaillerie worker --loglevel=info

# Démarrer Celery Beat (tâches planifiées)
celery -A quincaillerie beat --loglevel=info
```

## 📝 API Endpoints

### Produits
- `GET /produits/` - Liste des produits
- `POST /produits/create/` - Créer un produit
- `GET /produits/{id}/` - Détail d'un produit
- `PUT /produits/{id}/edit/` - Modifier un produit
- `DELETE /produits/{id}/delete/` - Supprimer un produit

### Stock
- `GET /stocks/` - Liste des mouvements
- `POST /stocks/entree/` - Entrée de stock
- `POST /stocks/sortie/` - Sortie de stock
- `POST /stocks/ajustement/` - Ajustement de stock

### Ventes
- `GET /ventes/` - Liste des ventes
- `POST /ventes/create/` - Créer une vente
- `GET /ventes/{id}/` - Détail d'une vente
- `POST /ventes/{id}/finaliser/` - Finaliser une vente

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Commit les changements (`git commit -am 'Ajouter nouvelle fonctionnalité'`)
4. Push vers la branche (`git push origin feature/nouvelle-fonctionnalite`)
5. Créer une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 📞 Support

Pour toute question ou problème :
- Créer une issue sur GitHub
- Contacter l'équipe de développement

---

**Développé avec ❤️ pour la gestion moderne de quincaillerie**
