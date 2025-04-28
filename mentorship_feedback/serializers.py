from rest_framework import serializers
from mentorship_feedback.models import Review


class ReviewSerializers(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['mentorship', 'comment', 'rating']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')

        if request:
            mentee_id = request.user.id
            if mentee_id:
                self.fields['mentorship'].queryset = self.fields['mentorship'].queryset.filter(mentee_id=mentee_id)
