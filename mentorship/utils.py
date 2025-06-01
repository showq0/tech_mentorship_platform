from django_celery_beat.models import ClockedSchedule, PeriodicTask
from rest_framework.utils.serializer_helpers import ReturnDict
import json
from datetime import timedelta, datetime
from user_auth.models import User
from django.db.models.functions import Cast
from django.db import models
from sentence_transformers import SentenceTransformer, util
from django.db.models import TextField
import json
import gc


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


class SentenceTransformerManager:
    def __init__(self, model_name):
        self.model_name = model_name

    def __enter__(self):
        self.model = SentenceTransformer(self.model_name)
        return self.model

    def __exit__(self, exc_type, exc_value, traceback):
        del self.model
        gc.collect()


def match_the_right_mentor(mentee: User):

    mentee_profile_info = json.dumps(mentee.profile_info)

    mentors = User.objects.filter(role="mentor")
    mentors_profile_info = list(
        mentors.annotate(
            profile_info_text=Cast('profile_info', TextField())
        ).values_list('profile_info_text', flat=True)
    )
    if not mentors_profile_info:
        return None

    with SentenceTransformerManager('sentence-transformers/all-MiniLM-L6-v2') as model:
        mentee_embedding = model.encode(mentee_profile_info, convert_to_tensor=True)
        mentor_embeddings = model.encode(mentors_profile_info, convert_to_tensor=True)
        cosine_scores = util.cos_sim(mentee_embedding, mentor_embeddings)
        best_index = cosine_scores.argmax().item()
        return mentors[best_index]