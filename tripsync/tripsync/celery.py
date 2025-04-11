import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tripsync.settings')

app = Celery('tripsync')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

from celery.schedules import crontab
# app.conf.CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

# Task Scheduling
app.conf.beat_schedule = {
    'add-every-60-seconds': {
        'task': 'apps.trips.tasks.delete_blacklisted_tokens',
        # 'schedule': 60.0
        'schedule': crontab(minute='*/1'),
    },
}
app.conf.timezone = 'UTC'