# Guide de Traduction - Multilingue (Français/Anglais)

## Configuration terminée ✅

Le système de traduction multilingue est maintenant configuré. Voici ce qui a été fait :

### 1. Configuration Django i18n
- ✅ Middleware de locale ajouté
- ✅ Langues supportées : Français (fr) et Anglais (en)
- ✅ Context processor i18n activé
- ✅ Sélecteur de langue dans la navbar

### 2. Structure créée
- ✅ Répertoire `locale/` créé
- ✅ Vue `SetLanguageView` pour changer la langue
- ✅ Route `/dashboard/set-language/` configurée

## Étapes pour créer les traductions

### Étape 1 : Générer les fichiers de traduction

```bash
# Créer les fichiers .po pour le français
python manage.py makemessages -l fr --ignore=venv --ignore=staticfiles

# Créer les fichiers .po pour l'anglais
python manage.py makemessages -l en --ignore=venv --ignore=staticfiles
```

### Étape 2 : Éditer les fichiers de traduction

Ouvrez et éditez les fichiers :
- `locale/fr/LC_MESSAGES/django.po` (pour le français - déjà traduit)
- `locale/en/LC_MESSAGES/django.po` (pour l'anglais - à traduire)

Exemple de traduction dans le fichier `.po` :
```
#: templates/base/base.html:50
msgid "Dashboard"
msgstr "Dashboard"

#: templates/base/base.html:59
msgid "Produits"
msgstr "Products"
```

### Étape 3 : Compiler les traductions

```bash
python manage.py compilemessages
```

### Étape 4 : Redémarrer le serveur

```bash
python manage.py runserver
```

## Utilisation dans les templates

Pour traduire du texte dans les templates, utilisez :

```django
{% load i18n %}

{% trans "Texte à traduire" %}
```

Exemple :
```django
<h1>{% trans "Gestion des Produits" %}</h1>
<p>{% trans "Bienvenue" %}</p>
```

## Utilisation dans Python

Dans les vues Python, utilisez :

```python
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy as _

# Exemple
message = _("Utilisateur créé avec succès")
```

## Sélecteur de langue

Le sélecteur de langue est maintenant visible dans la navbar (en haut à droite).

L'utilisateur peut changer de langue en sélectionnant FR ou EN, et la préférence est sauvegardée dans la session.

## Notes importantes

- Les traductions sont stockées dans `locale/{lang}/LC_MESSAGES/django.po`
- Après modification des fichiers `.po`, il faut compiler avec `compilemessages`
- La langue par défaut est le français (fr)
- Le changement de langue persiste pendant toute la session

