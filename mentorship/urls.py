from django.urls import path
from mentorship.views import MentorListView, MenteeListView
urlpatterns = [

    path('mentors/', MentorListView.as_view(), name="mentor"),
    path('mentor/<int:id>/', MenteeListView.as_view(), name='mentee-detail'),
    path('mentees/', MenteeListView.as_view(), name="mentee"),
    path('mentee/<int:id>/', MenteeListView.as_view(), name='mentee-detail'),

]
