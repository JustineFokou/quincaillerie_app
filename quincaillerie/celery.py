import os
from celery import Celery

# Configuration Django pour Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quincaillerie.settings')

app = Celery('quincaillerie')

# Configuration Celery depuis les settings Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Découverte automatique des tâches dans les applications Django
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
