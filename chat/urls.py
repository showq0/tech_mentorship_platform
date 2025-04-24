
from django.urls import path
from chat.views import ConversationsListView, ChatRoomView
urlpatterns = [
    path('user_chats/', ConversationsListView.as_view(), name="user_chats"),
    # path('messages/<int:user_id>', MessagesListView.as_view(), name="messages")
    path('chat_room/<int:chat_id>/', ChatRoomView.as_view(), name='chat_room_view'),

]