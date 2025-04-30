from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tech_mentorship_platform.settings')

# Create Celery app
app = Celery('tech_mentorship_platform')

app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks in all installed apps
app.autodiscover_tasks()
