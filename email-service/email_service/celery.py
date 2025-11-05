"""
Celery configuration for email_service.
"""
import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'email_service.settings')

app = Celery('email_service')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# Configure task routes
app.conf.task_routes = {
    'notifications.tasks.send_email_task': {'queue': 'emails'},
    'notifications.tasks.send_notification_task': {'queue': 'notifications'},
}

# Configure task retry settings
app.conf.task_default_retry_delay = 5  # 5 seconds
app.conf.task_max_retries = 3

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
