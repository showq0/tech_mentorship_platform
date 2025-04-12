from django.urls import path, include
from mentorship.views import CreateAvailableSlotsView, BookSessionView, AssignMentorView, MentorViewSet, MenteeViewSet
from rest_framework.routers import DefaultRouter


urlpatterns = [
    path('mentors/', MentorViewSet.as_view(), name='mentor'),
    path('mentees/', MenteeViewSet.as_view(), name='mentee'),
    path('create_slots/<int:mentor_id>', CreateAvailableSlotsView.as_view(), name='create_slots'),
    path('book_session/<int:mentee_id>/<int:mentor_id>', BookSessionView.as_view(), name='book_session'),
    path('assign_mentor/<int:mentee_id>/', AssignMentorView.as_view(), name='assign_mentor'),
]
