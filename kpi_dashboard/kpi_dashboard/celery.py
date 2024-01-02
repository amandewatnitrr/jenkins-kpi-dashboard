from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kpi_dashboard.settings')

app = Celery('kpi_dashboard')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

# Periodic task configuration
app.conf.beat_schedule = {
    'update-gitlab-data': {
        'task': 'kpi_dashboard.views.update_gitlab_data',
        'schedule': 60.0,  # Run every 60 seconds (adjust as needed)
    },
}