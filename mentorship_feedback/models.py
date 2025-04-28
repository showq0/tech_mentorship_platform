from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from mentorship.models import Mentorship
# Create your models here.


class Review(models.Model):
    mentorship = models.OneToOneField(Mentorship, on_delete=models.CASCADE)
    comment = models.CharField(max_length=255)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.mentorship.mentee.username} review {self.mentorship.mentor.username} '


