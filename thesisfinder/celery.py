import os
from celery import Celery

# Définir les paramètres Django pour Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'thesisfinder.settings')

app = Celery('thesisfinder')

# Charger la configuration Celery depuis settings.py
app.config_from_object('django.conf:settings', namespace='CELERY')

# Découvrir automatiquement les tâches dans les applications Django
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
