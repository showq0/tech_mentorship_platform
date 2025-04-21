from django.db import models
from mentorship.models import User
from django.db.models import Q


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='message_sender',
                               )

    receiver = models.ForeignKey(User, on_delete=models.CASCADE,
                                 related_name='message_receiver',
                                 )
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-sent_at']

    def __str__(self):
        return f"{self.content}"

    @classmethod
    def chat(cls, user1_id, user2_id ):
        chat_users = [user1_id, user2_id]
        chat_messages = Message.objects.filter(sender__in=chat_users, receiver__in=chat_users)
        return chat_messages

    @classmethod
    def get_chat_partners(cls, user):
        users = User.objects.filter(
            Q(id__in=Message.objects.filter(sender=user.id).values('receiver')) |
            Q(id__in=Message.objects.filter(receiver=user.id).values('sender'))
        ).distinct()
        return users
