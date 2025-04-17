from rest_framework import serializers
from mentorship.models import Session, Mentorship
from user_auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'profile_info']


class BookSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ['slot']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')

        if request:
            url_kwargs = request.parser_context.get('kwargs', {})
            mentor_id = url_kwargs.get('mentor_id')
            if mentor_id:
                self.fields['slot'].queryset = self.fields['slot'].queryset.filter(mentor_id=mentor_id, is_booked=False)


class SlotSerializer(serializers.Serializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    start_time = serializers.TimeField()
    end_time = serializers.TimeField()
    duration_minutes = serializers.IntegerField()
    buffer_minutes = serializers.IntegerField()

    def validate(self, data):
        if data['end_date'] < data['start_date']:
            raise serializers.ValidationError("The last date must be after the first date.")
        return data


class AssignMentorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mentorship
        fields = ['mentor']
