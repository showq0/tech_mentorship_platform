from django.urls import path
from mentorship_feedback.views import MentorReviews, CreateReview


urlpatterns = [
    path('reviews/', MentorReviews.as_view(), name="mentor_reviews"),
    path('give-feedback/', CreateReview.as_view(), name="give_feedback")

]