from rest_framework import serializers
from chat.models import Message, User


class MessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
