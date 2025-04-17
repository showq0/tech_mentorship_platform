from rest_framework import serializers
from mentorship.models import User, Session, Mentorship


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
            mentee_id = request.user.id
            # Filtering slots based on mentor_id param
            url_kwargs = request.parser_context.get('kwargs', {})
            mentor_id = url_kwargs.get('mentor_id')
            # need to indexing by mentor
            is_mentorship = Mentorship.objects.filter(mentee_id=mentee_id, mentor_id=mentor_id, status='active').exists()
            if not is_mentorship:
                self.fields['slot'].queryset = None

            if is_mentorship:
                self.fields['slot'].queryset = self.fields['slot'].queryset.filter(mentor_id=mentor_id,is_booked=False)


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
