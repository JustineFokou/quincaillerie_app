from celery.schedules import crontab

# Configuration des tâches planifiées Celery Beat
CELERY_BEAT_SCHEDULE = {
    'check-stock-alerts': {
        'task': 'core.tasks.check_stock_alerts',
        'schedule': crontab(hour=9, minute=0),  # Tous les jours à 9h00
    },
    'generate-daily-report': {
        'task': 'core.tasks.generate_daily_report',
        'schedule': crontab(hour=18, minute=0),  # Tous les jours à 18h00
    },
}
