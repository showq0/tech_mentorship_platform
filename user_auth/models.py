from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    MENTOR = 'mentor'
    MENTEE = 'mentee'
    ROLE_CHOICES = [
        (MENTOR, 'Mentor'),
        (MENTEE, 'Mentee'),
    ]

    role = models.CharField(
        max_length=6,
        choices=ROLE_CHOICES,
        blank=True,
    )
    profile_info = models.JSONField(default=dict)

    def __str__(self):
        if self.role:
            return f"{self.username}-{self.role}"
        return f"{self.username}"