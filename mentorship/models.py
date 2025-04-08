from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

# Create your models here.

PENDING = 'pending'
ACTIVE = 'active'
COMPLETED = 'completed'

STATUS_CHOICES = [
    (PENDING, 'Pending'),
    (ACTIVE, 'Active'),
    (COMPLETED, 'Completed'),
]


class Mentor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_mentor')
    skills = models.TextField()  # Comma-separated list of skills
    bio = models.TextField()

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('mentor_detail', args=[str(self.id)])


class Mentee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_mentee')
    interest = models.CharField(max_length=100)
    goals = models.TextField()

    def __str__(self):
        return self.user.username


class Mentorship(models.Model):
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)
    mentee = models.ForeignKey(Mentee, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def __str__(self):
        if self.end_date:
            return f"{self.mentee.user.username} - {self.end_date}"
        return f"{self.mentee.user.username} - active"

