from django.test import TestCase
from django_celery_beat.models import ClockedSchedule, PeriodicTask
from django.utils import timezone
from mentorship.models import Session, User, BookingSlot
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


class MatchMentorTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create mentor users
        cls.mentor1 = User.objects.create(
            username="mentor1",
            role="mentor",
            profile_info={"bio": "Frontend expert but love backend topics and AI.", "skills": ["JavaScript", "React", "CSS"], "mentorship_style": "Supportive and collaborative."}
        )
        cls.mentor2 = User.objects.create(
            username="mentor2",
            role="mentor",
            profile_info={"bio": "Experienced backend developer and AI", "skills": ["Python", "Django", "REST APIs"], "mentorship_style": "Hands-on and project-based."}
        )
        cls.mentor2 = User.objects.create(
            username="mentor3",
            role="mentor",
            profile_info={"bio": "Cloud and DevOps specialist.", "skills": ["AWS", "Kubernetes", "Terraform"],"contact_info": "rima@example.com", "mentorship_style": "Structured and goal-oriented"}
        )

        # Create mentee user
        cls.mentee = User.objects.create(
            username="mentee1",
            role="mentee",
            profile_info={"bio": "Passionate about AI.", "goals": ["Learn python", "AI"], "current_skills": ["Python"], "mentorship_needs": "Hands-on project"}
        )

    def test_match_the_right_mentor(self):
        from mentorship.utils import match_the_right_mentor

        result = match_the_right_mentor(self.mentee)
        best_mentor = result.get('mentor')
        self.assertIsNotNone(best_mentor)
        print(f"Best matched mentor: {best_mentor.username}")
        self.assertEqual(best_mentor.username, "mentor2")

