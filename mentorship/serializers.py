from rest_framework import serializers
from mentorship.models import Session, Mentorship, BookingSlot
from user_auth.models import User
from user_auth.serializers import UserSerializer


class UserListSerializer(serializers.ModelSerializer):
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


class BookingSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingSlot
        fields = ['start_time', 'duration_minutes']


class SessionSerializer(serializers.ModelSerializer):
    mentor = UserSerializer()
    mentee = UserSerializer()
    slot = BookingSlotSerializer()

    class Meta:
        model = Session
        fields = ['mentor', 'mentee', 'slot', 'id']
        depth = 1


