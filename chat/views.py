from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from mentorship.serializers import UserSerializer
from chat.models import Message, Chat, User
from chat.pagination import ViewPagination


class ConversationsListView(ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = ViewPagination

    def get_queryset(self):
        if self.request.user:
            return Chat.get_user_chats(self.request.user)
        return []

