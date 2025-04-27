from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from user_auth.views import RegisterView,ProfileView

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),# login
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # url(r'^api/v1/', include('rest_framework.urls'), name="rest_api")
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view() ,name="profile")

]
