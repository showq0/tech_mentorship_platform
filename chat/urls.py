from django.urls import path
from chat.views import ConversationsListView, MessagesListView

urlpatterns = [
    path('conversations/', ConversationsListView.as_view(), name="conversations"),
    path('messages/<int:user_id>', MessagesListView.as_view(), name="messages")

]
