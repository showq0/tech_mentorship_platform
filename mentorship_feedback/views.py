from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from mentorship_feedback.models import Review, Mentorship
from rest_framework.permissions import IsAuthenticated
from mentorship.permissions import IsMentor, IsMentee
from mentorship_feedback.serializers import ReviewSerializers
from django.core.exceptions import ValidationError


# Create your views here.


class MentorReviews(ListAPIView):
    permission_classes = [IsAuthenticated, IsMentor]
    serializer_class = ReviewSerializers

    def get_queryset(self):
        if self.request.user:
            mentorship_list = Mentorship.objects.filter(mentor=self.request.user)
            return Review.objects.filter(mentorship__in=mentorship_list)
        return []


class CreateReview(APIView):
    permission_classes = [IsAuthenticated, IsMentee]
    serializer_class = ReviewSerializers

    def post(self, request):
        serializer = ReviewSerializers(data=request.data)
        user_id = request.user.id
        if serializer.is_valid():
            mentorship_id = serializer.validated_data['mentorship'].id
            mentee_id = Mentorship.objects.get(id=mentorship_id).mentee_id
            if mentee_id != user_id:
                return Response({"message": "You don't have access to review other mentors"},
                                status=status.HTTP_401_UNAUTHORIZED)
            serializer.save()
            return Response({"message": "Review sent successfully"},
                            status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
