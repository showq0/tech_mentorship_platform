from django_celery_beat.models import ClockedSchedule, PeriodicTask
from rest_framework.utils.serializer_helpers import ReturnDict
import json


def schedule_session_reminder(session: ReturnDict):
    session_time = session['slot']['start_time']
    mentor, mentee = session['mentor']['username'], session['mentor']['username']

    clocked_schedule = ClockedSchedule.objects.create(clocked_time=session_time)

    PeriodicTask.objects.create(
        clocked=clocked_schedule,
        name=f'session_reminder-{mentor}-{mentee}-{session_time}',
        task='mentorship.tasks.send_reminder_emails',
        one_off=True,
        args=json.dumps([session]),
    )
