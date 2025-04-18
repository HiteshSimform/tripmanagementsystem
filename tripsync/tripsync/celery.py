import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tripsync.settings")

app = Celery("tripsync")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


# Task Scheduling
app.conf.beat_schedule = {
    "add-every-60-seconds": {
        "task": "apps.authentication.tasks.delete_blacklisted_tokens",
        # 'schedule': 60.0
        "schedule": crontab(minute="*/1"),
    },
    "send-trip-reminder-emails": {
        "task": "apps.trips.tasks.send_trip_reminder_email",
        "schedule": crontab(minute="*/1"),
        "args": (1,),
    },
}
app.conf.timezone = "UTC"
