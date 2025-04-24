
from django.urls import path
from chat.views import ConversationsListView, chat_room_view
urlpatterns = [
    path('users_chats/', ConversationsListView.as_view(), name="users_chats"),
    # path('messages/<int:user_id>', MessagesListView.as_view(), name="messages")
    path('chat_room/<int:mentorship_id>/', chat_room_view, name='chat_room_view'),

]