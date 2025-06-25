#!/bin/sh

exec gunicorn tech_mentorship_platform.wsgi:application --bind 0.0.0.0:8000

exec celery -A tech_mentorship_platform worker --loglevel=info
exec celery -A tech_mentorship_platform beat --loglevel=info
