from django.contrib.auth.models import User
from mentorship.models import Mentor, Mentee
from rest_framework import serializers


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=[
        ('mentor', 'Mentor'),
        ('mentee', 'Mentee')
    ])

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        if validated_data['role'] == 'mentor':
            user = Mentor.objects.create(
                user_id = user.id,
            )
        if validated_data['role'] == 'mentee':
            user = Mentee.objects.create(
                user_id = user.id,
            )
        return user
