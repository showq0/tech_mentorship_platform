from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError


# Create your models here.

PENDING = 'pending'
ACTIVE = 'active'
COMPLETED = 'completed'

STATUS_CHOICES = [
    (PENDING, 'Pending'),
    (ACTIVE, 'Active'),
    (COMPLETED, 'Completed'),
]


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


class Mentorship(models.Model):
    mentor = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='mentorship_as_mentor',
                               limit_choices_to={'role': 'mentor'})
    mentee = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='mentorship_as_mentee',
                               limit_choices_to={'role': 'mentee'})
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def clean(self):
        if self.mentor and self.mentor.role != 'mentor':
            raise ValidationError("mentor should be user with mentor role")
        if self.mentee and self.mentee.role != 'mentee':
            raise ValidationError("mentee should be user with mentee role")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        if self.end_date:
            return f"{self.mentee.username} - {self.end_date}"
        return f"{self.mentee.username} - active"

    class Meta:
        unique_together = ['mentor', 'mentee']


class BookingSlot(models.Model):
    mentor = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField(default=timezone.now)
    duration_minutes = models.PositiveIntegerField()
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.mentor}-{self.start_time}"

    class Meta:
        unique_together = ['mentor', 'start_time']


class Session (models.Model):
    mentor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='session_as_mentor')
    mentee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='session_as_mentee')
    slot = models.OneToOneField(BookingSlot, on_delete=models.CASCADE)
    note = models.TextField(blank=True, default="")

    class Meta:
        unique_together = ['mentor', 'mentee', 'slot']

    def __str__(self):

        return f"{self.mentor.username}-{self.mentee.username}-{self.slot.start_time}"
