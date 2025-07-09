import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Email_campaign.settings")
app = Celery("Email_campaign")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
