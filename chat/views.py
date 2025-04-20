from django.shortcuts import render
from rest_framework.generics import ListAPIView
from chat.serializers import MessagesSerializer
from rest_framework.permissions import IsAuthenticated
from mentorship.serializers import UserSerializer
from chat.models import Message, User
from chat.pagination import ViewPagination

# Create your views here.


class ConversationsListView(ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = ViewPagination

    def get_queryset(self):
        if self.request.user:
            return Message.get_chat_partners(self.request.user)
        return []


class MessagesListView(ListAPIView):
    serializer_class = MessagesSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = ViewPagination

    def get_queryset(self):
        messages = None

        if self.request.user:
            messages = Message.chat(self.request.user, self.kwargs['user_id'])
        return messages
