from celery import shared_task
from django.core.mail import send_mail


def send_reminder_email(username, user_email, participant, session):
    start_time = session['start_time']
    duration = session['duration_minutes']

    send_mail(
        'Reminder',
        f'''Hi {username},
Just a quick reminder that you have a scheduled session with  {participant} coming up soon.
Session Details:
Date-time: {start_time}
Duration: {duration}''',
        'tech_mentorship_platform@gmail.com',
        [user_email],

        fail_silently=False,
    )


@shared_task
def send_reminder_emails(session: dict):
    slot = session['slot']
    mentor, mentee = session['mentor']['username'], session['mentee']['username']
    mentor_email = session['mentor']['email']
    mentee_email = session['mentee']['email']

    # send to mentor
    send_reminder_email(mentor, mentor_email, mentee, slot)
    # send to mentee
    send_reminder_email(mentee, mentee_email, mentor, slot)

