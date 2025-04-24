from django.db import models
from mentorship.models import User, Mentorship


class Chat(models.Model):
    start_at = models.DateTimeField(auto_now_add=True)
    mentorship = models.OneToOneField(Mentorship, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.mentorship.mentee.username}-{self.mentorship.mentor.username}"

    class Meta:
        ordering = ['-start_at']

    @classmethod
    def get_user_chats(cls, user):
        users = []
        if user.role == "mentor":
            user_chats = Chat.objects.filter(
                mentorship__in=Mentorship.objects.filter(mentor=user)
            )
            for chat in user_chats:
                users.append(chat.mentorship.mentee)

        if user.role == "mentee":
            user_chats = Chat.objects.filter(
                mentorship__in=Mentorship.objects.filter(mentee=user)
            )
            for chat in user_chats:
                users.append(chat.mentorship.mentor)

        return users


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()

    is_read = models.BooleanField(default=False)
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-sent_at']

    def __str__(self):
        return f"{self.content}"
