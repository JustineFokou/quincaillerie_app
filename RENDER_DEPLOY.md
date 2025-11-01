# Guide de Déploiement sur Render

Ce guide vous explique comment déployer l'application Quincaillerie sur Render.

## 📋 Prérequis

1. Un compte Render (gratuit disponible)
2. Un compte GitHub (pour le repository)

## 🚀 Étapes de Déploiement

### 1. Préparer le Repository GitHub

1. Créez un repository GitHub (si ce n'est pas déjà fait)
2. Commitez et poussez votre code :
   ```bash
   git add .
   git commit -m "Prepare for Render deployment"
   git push origin main
   ```

### 2. Créer un Service Web sur Render

1. Allez sur [Render Dashboard](https://dashboard.render.com/)
2. Cliquez sur **"New +"** → **"Web Service"**
3. Connectez votre repository GitHub
4. Configurez le service :
   - **Name**: `quincaillerie-app` (ou votre choix)
   - **Region**: `Frankfurt` (ou celui de votre choix)
   - **Branch**: `main` (ou votre branche principale)
   - **Root Directory**: `.` (laisser vide si à la racine)
   - **Runtime**: `Python 3`
   - **Build Command**: 
     ```bash
     pip install --upgrade pip && pip install -r requirements.txt && python manage.py migrate --noinput && python manage.py collectstatic --noinput
     ```
   - **Start Command**: 
     ```bash
     gunicorn quincaillerie.wsgi:application --bind 0.0.0.0:$PORT
     ```

### 3. Créer une Base de Données PostgreSQL

1. Dans Render Dashboard, cliquez sur **"New +"** → **"PostgreSQL"**
2. Configurez :
   - **Name**: `quincaillerie-db`
   - **Plan**: `Starter` (gratuit)
   - **Region**: Même région que votre service web
3. Copiez la **Connection String** (Internal Database URL)

### 4. Créer Redis (Optionnel - pour Celery)

Si vous utilisez Celery :
1. Cliquez sur **"New +"** → **"Redis"**
2. Configurez :
   - **Name**: `quincaillerie-redis`
   - **Plan**: `Starter` (gratuit)
3. Copiez l'URL Redis

### 5. Configurer les Variables d'Environnement

Dans votre service web, allez dans **Environment** et ajoutez :

#### Variables Requises :

```
PYTHON_VERSION=3.10.12
DEBUG=False
SECRET_KEY=votre-secret-key-tres-long-et-aleatoire
ALLOWED_HOSTS=votre-app.onrender.com,localhost
DATABASE_URL=<Internal Database URL de votre PostgreSQL>
```

#### Variables Optionnelles (si vous utilisez Celery) :

```
CELERY_BROKER_URL=redis://red-xxxxx:6379/0
CELERY_RESULT_BACKEND=redis://red-xxxxx:6379/0
```

#### Générer un SECRET_KEY sécurisé :

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 6. Déployer

1. Cliquez sur **"Manual Deploy"** → **"Deploy latest commit"**
2. Attendez que le build se termine (5-10 minutes la première fois)
3. Votre application sera disponible sur : `https://votre-app.onrender.com`

### 7. Créer un Superutilisateur

Une fois déployé, connectez-vous au shell de votre service :

1. Dans Render Dashboard → Votre service → **Shell**
2. Exécutez :
   ```bash
   python manage.py createsuperuser
   ```
3. Suivez les instructions pour créer votre compte admin

## 🔧 Utilisation de render.yaml (Méthode Alternative)

Si vous préférez utiliser le fichier `render.yaml` :

1. Modifiez `render.yaml` avec vos valeurs
2. Dans Render Dashboard → **"New +"** → **"Blueprint"**
3. Connectez votre repository
4. Render créera automatiquement tous les services

⚠️ **Important** : Remplacez `your-app-name.onrender.com` par votre nom d'application réel dans `render.yaml`

## 📝 Notes Importantes

### Static Files
- Les fichiers statiques sont servis par WhiteNoise (déjà configuré)
- `collectstatic` est exécuté automatiquement lors du build

### Base de Données
- Utilisez l'**Internal Database URL** (pas l'External) pour de meilleures performances
- Les migrations sont exécutées automatiquement lors du build

### Media Files
- Pour les fichiers media (images uploadées), utilisez un service de stockage comme AWS S3, Cloudinary, ou Render Disk
- Actuellement, les fichiers sont stockés localement (non persistant sur Render)

### Debugging
- Mettez `DEBUG=False` en production
- Consultez les logs dans Render Dashboard → Votre service → **Logs**

## 🐛 Dépannage

### Erreur "No such file or directory"
- Vérifiez que le `Procfile` est à la racine du projet
- Vérifiez que le chemin dans `startCommand` est correct

### Erreur de base de données
- Vérifiez que `DATABASE_URL` est bien configuré
- Vérifiez que les migrations ont été exécutées

### Erreur 500
- Vérifiez les logs dans Render Dashboard
- Assurez-vous que `DEBUG=False` et `ALLOWED_HOSTS` est correctement configuré

## 🔒 Sécurité

- ✅ `DEBUG=False` en production
- ✅ `SECRET_KEY` unique et sécurisé
- ✅ `ALLOWED_HOSTS` configuré
- ✅ HTTPS activé automatiquement sur Render
- ✅ Variables d'environnement sécurisées

## 📚 Ressources

- [Documentation Render](https://render.com/docs)
- [Déploiement Django sur Render](https://render.com/docs/deploy-django)
- [PostgreSQL sur Render](https://render.com/docs/databases)

