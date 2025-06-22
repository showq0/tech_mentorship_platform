from django_celery_beat.models import ClockedSchedule, PeriodicTask
from rest_framework.utils.serializer_helpers import ReturnDict
from datetime import timedelta, datetime
from user_auth.models import User
from django.db.models.functions import Cast
from sentence_transformers import SentenceTransformer, util
from django.db.models import TextField
import json
import gc
import torch


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
    mentee_profile_info = mentee.profile_info
    goals = mentee_profile_info.get("goals", "")
    mentorship_needs = mentee_profile_info.get("mentorship_needs", "")
    current_skills = mentee_profile_info.get("current_skills", [])
    mentors = User.objects.filter(role="mentor")
    mentors_profile_info = list(
        mentors.annotate(
            profile_info_text=Cast('profile_info', TextField())
        ).values_list('profile_info_text', flat=True)
    )

    if not mentors_profile_info:
        return None

    with SentenceTransformerManager('sentence-transformers/all-mpnet-base-v2') as model:
        mentor_embeddings = model.encode(mentors_profile_info, convert_to_tensor=True)

        goals_embeddings = model.encode(goals, convert_to_tensor=True)
        current_skills_embeddings = model.encode(current_skills, convert_to_tensor=True)
        mentorship_needs_embeddings = model.encode(mentorship_needs, convert_to_tensor=True)

        goals_scores = util.semantic_search(goals_embeddings, mentor_embeddings)
        current_skills_score = util.semantic_search(current_skills_embeddings, mentor_embeddings)
        mentorship_need_scores = util.semantic_search(mentorship_needs_embeddings, mentor_embeddings)
        threshold = torch.quantile(goals_scores, 0.75).item()

        filtered_goals_scores = goals_scores.where(goals_scores > threshold, 0)
        final_score = filtered_goals_scores*(current_skills_score*0.5 + mentorship_need_scores*0.5)

        best_index = final_score.argmax().item()
        mentor = mentors[best_index]

        return {
            "mentor": mentor,
            "scores": {
                "goals_score": goals_scores[0][best_index].item(),
                "skills_score": current_skills_score[0][best_index].item(),
                "needs_score": mentorship_need_scores[0][best_index].item(),
                "final_score": final_score[0][best_index].item()
            }
        }
