from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from mentorship.models import Session
from mentorship.serializers import SessionSerializer
from mentorship.utils import schedule_session_reminder
from django_celery_beat.models import PeriodicTask


@receiver(post_save, sender=Session)
def after_session_saved(sender, instance, created, **kwargs):

    if created:
        serializer = SessionSerializer(instance=instance)
        data = serializer.data
        schedule_session_reminder(data)


@receiver(post_delete, sender=Session)
def after_session_deleted(sender, instance, **kwargs):
    mentor = instance.mentor.username
    mentee = instance.mentee.username
    start_time = instance.slot.start_time
    try:
        task_name = f'session_reminder-{mentor}-{mentee}-{start_time}'
        task = PeriodicTask.objects.get(name=task_name)
        clocked = task.clocked
        if clocked:
            clocked.delete()
        task.delete()
    except PeriodicTask.DoesNotExist:
        pass
