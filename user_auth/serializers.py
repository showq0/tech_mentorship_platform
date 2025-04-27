from user_auth.models import User
from rest_framework import serializers
from django_jsonform.validators import JSONSchemaValidator, JSONSchemaValidationError
from user_auth.constant import mentee_profile_info, mentor_profile_info


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
            password=validated_data['password'],
            role=validated_data['role']
        )
        return user


class ProfileSerializer(serializers.Serializer):
    profile_info = serializers.JSONField()

    def validate_profile_info(self, profile_info):
        is_mentor = self.context.get('is_mentor')
        if is_mentor:
            validator = JSONSchemaValidator(mentor_profile_info)
        else:
            validator = JSONSchemaValidator(mentee_profile_info)

        validator(profile_info)

        return profile_info
