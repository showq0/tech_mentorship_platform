from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
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
    skills = models.TextField(blank=True, default="")
    bio = models.TextField(blank=True, default="")

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('mentor_detail', args=[str(self.id)])


class Mentee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_mentee')
    interest = models.CharField(max_length=100, blank=True, default="")
    goals = models.TextField(blank=True, default="")

    def __str__(self):
        return self.user.username


class Mentorship(models.Model):
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)
    mentee = models.ForeignKey(Mentee, on_delete=models.CASCADE, related_name='mentorship')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        if self.end_date:
            return f"{self.mentee.user.username} - {self.end_date}"
        return f"{self.mentee.user.username} - active"

    class Meta:
        unique_together = ['mentor', 'mentee']


class BookingSlot(models.Model):
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)
    start_time = models.DateTimeField(default=timezone.now)
    duration_minutes = models.PositiveIntegerField()
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.mentor}-{self.start_time}"

    class Meta:
        unique_together = ['mentor', 'start_time']


class Session (models.Model):
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)
    mentee = models.ForeignKey(Mentee, on_delete=models.CASCADE)
    slot = models.OneToOneField(BookingSlot, on_delete=models.CASCADE)
    note = models.TextField(blank=True, default="")

    class Meta:
        unique_together = ['mentor', 'mentee', 'slot']

    def __str__(self):

        return f"{self.mentor.user.username}-{self.mentee.user.username}-{self.slot.start_time}"
