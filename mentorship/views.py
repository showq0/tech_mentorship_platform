from django.shortcuts import render
from mentorship.models import Mentor, Mentee
from mentorship.serializers import MentorSerializer, MenteeSerializer
from rest_framework.generics import ListAPIView
from django.http import Http404, HttpResponse, JsonResponse
from rest_framework.response import Response

# Create your views here.


class MentorListView(ListAPIView):
    queryset = Mentor.objects.all()
    serializer_class = MentorSerializer

    def get_queryset(self):
        mentor_id = self.kwargs.get('id')
        if mentor_id:
            return Mentor.objects.filter(id=mentor_id)
        return Mentor.objects.all()


class MenteeListView(ListAPIView):
    queryset = Mentee.objects.all()
    serializer_class = MenteeSerializer

    def get_queryset(self):
        mentee_id = self.kwargs.get('id')
        if mentee_id:
            return Mentee.objects.filter(id=mentee_id)
        return Mentee.objects.all()
