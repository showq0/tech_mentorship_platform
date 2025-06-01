from django.urls import path, include
from mentorship.views import CreateAvailableSlotsView, BookSessionView, RequestMentorshipView, MentorListView, MenteeListView, match_mentor
from rest_framework.routers import DefaultRouter


urlpatterns = [
    path('mentors/', MentorListView.as_view(), name='mentors'),
    path('mentees/', MenteeListView.as_view(), name='mentees'),
    path('mentor/availability/', CreateAvailableSlotsView.as_view(), name='mentor-availability-create'),
    path('mentors/<int:mentor_id>/sessions/book/', BookSessionView.as_view(), name='session-book'),
    path('mentors/<int:mentor_id>/requests/', RequestMentorshipView.as_view(), name='mentorship-request'),
    path('best-mentors/', match_mentor,  name='best-mentore'),

]