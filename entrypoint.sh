#!/bin/sh
python manage.py collectstatic --noinput

# Start Celery in background
celery -A tech_mentorship_platform worker --loglevel=info &
celery -A tech_mentorship_platform beat --loglevel=info &

# Start the ASGI server
exec daphne -b 0.0.0.0 -p 8000 tech_mentorship_platform.asgi:application
