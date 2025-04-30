from django_celery_beat.models import ClockedSchedule, PeriodicTask
from rest_framework.utils.serializer_helpers import ReturnDict
import json
from datetime import timedelta, datetime


def schedule_session_reminder(session: ReturnDict):
    # iso format
    start_time = datetime.fromisoformat(session['slot']['start_time'])

    reminder_time = start_time - timedelta(minutes=30)
    mentor, mentee = session['mentor']['username'], session['mentee']['username']

    clocked_schedule = ClockedSchedule.objects.create(clocked_time=reminder_time)

    PeriodicTask.objects.create(
        clocked=clocked_schedule,
        name=f'session_reminder-{mentor}-{mentee}-{start_time}',
        task='mentorship.tasks.send_reminder_emails',
        one_off=True,
        args=json.dumps([session]),
    )
