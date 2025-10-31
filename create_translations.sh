#!/bin/bash
# Script pour créer les fichiers de traduction

echo "Creating translation files..."

# Créer les répertoires de locale
mkdir -p locale/fr/LC_MESSAGES
mkdir -p locale/en/LC_MESSAGES

# Créer les fichiers .po pour le français
django-admin makemessages -l fr --ignore=venv
django-admin makemessages -l en --ignore=venv

echo "Translation files created!"
echo "Now edit the .po files in locale/fr/LC_MESSAGES/django.po and locale/en/LC_MESSAGES/django.po"
echo "Then run: python manage.py compilemessages"

