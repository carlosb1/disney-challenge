import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'labhouse.settings')

from celery import Celery

app = Celery('labhouse')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


