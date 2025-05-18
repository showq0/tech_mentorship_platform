from django.test import TestCase
from django_celery_beat.models import ClockedSchedule, PeriodicTask
from django.utils import timezone
from mentorship.utils import schedule_session_reminder
from mentorship.models import Session, User, BookingSlot
from mentorship.serializers import SessionSerializer
import time
from datetime import timedelta
class ScheduleSessionReminderTest(TestCase):
    def setUp(self):

        mentor = User.objects.create_user(
            username='user1',
            email='email@gmail.com',
            password='user11',
            role='menotr'
        )
        mentee = User.objects.create_user(
            username='user2',
            email='email@gmail.com',
            password='user22',
            role='mentee'
        )
        slot = BookingSlot.objects.create(
            mentor=mentor,
            start_time=timezone.now(),
            duration_minutes=20,
        )
        Session.objects.create(
            mentor=mentor,
            mentee=mentee,
            slot=slot,
        )

    def test_schedule_session_reminder_creates_clocked_task(self):
        session = Session.objects.filter(mentor__username='user1', mentee__username='user2').first()
        session_time = session.slot.start_time
        reminder_time = session_time - timedelta(minutes=30)
        self.assertTrue(ClockedSchedule.objects.filter(clocked_time=reminder_time).exists())
        task_name = f'session_reminder-user1-user2-{session_time}'
        task = PeriodicTask.objects.get(name=task_name)
        self.assertEqual(task.task, 'mentorship.tasks.send_reminder_emails')
        self.assertTrue(task.one_off)