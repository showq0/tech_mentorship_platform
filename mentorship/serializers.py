from rest_framework import serializers
from mentorship.models import Mentor, Mentee, Session, Mentorship


class MentorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Mentor
        fields = ['user', 'skills', 'bio']


class MenteeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Mentee
        fields = ['user', 'interest', 'goals']


class BookSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ['slot']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        available_slot = self.fields['slot'].queryset.filter(is_booked=False)
        self.fields['slot'].queryset = available_slot

        request = self.context.get('request')

        if request:
            # Filtering slots based on mentor_id param
            url_kwargs = request.parser_context.get('kwargs', {})
            mentor_id = url_kwargs.get('mentor_id')
            if mentor_id:
                self.fields['slot'].queryset = available_slot.filter(mentor_id=mentor_id)


class SlotSerializer(serializers.Serializer):
    first_date = serializers.DateField()
    last_date = serializers.DateField()
    start_time = serializers.TimeField()
    end_time = serializers.TimeField()
    duration_minutes = serializers.IntegerField()
    buffer_minutes = serializers.IntegerField()

    def validate(self, data):
        if data['last_date'] < data['first_date']:
            raise serializers.ValidationError("The last date must be after the first date.")
        return data


class AssignMentorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mentorship
        fields = ['mentor']
