from rest_framework import serializers
from mentorship.models import Mentor, Mentee


class MentorSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')

    class Meta:
        model = Mentor
        fields = ['username', 'skills', 'bio']


class MenteeSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')

    class Meta:
        model = Mentee
        fields = ['username', 'interest', 'goals']