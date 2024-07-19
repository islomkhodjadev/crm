from __future__ import absolute_import, unicode_literals
import os
from celery import Celery


import eventlet
eventlet.monkey_patch()


# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'services.settings')

app = Celery('services')

# Load task modules from all registered Django app configs.
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


