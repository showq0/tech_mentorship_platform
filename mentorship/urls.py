from django.urls import path, include
from mentorship.views import CreateAvailableSlotsView, BookSessionView, AssignMentorView, MentorListView, MenteeListView
from rest_framework.routers import DefaultRouter


urlpatterns = [
    path('mentors/', MentorListView.as_view(), name='mentor'),
    path('mentees/', MenteeListView.as_view(), name='mentee'),
    path('create_slots/', CreateAvailableSlotsView.as_view(), name='create_slots'),
    path('book_session/<int:mentor_id>', BookSessionView.as_view(), name='book_session'),
    path('assign_mentor/', AssignMentorView.as_view(), name='assign_mentor'),
]
