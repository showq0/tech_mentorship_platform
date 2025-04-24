from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from mentorship.serializers import UserSerializer
from chat.models import Message, Chat
from chat.pagination import ViewPagination
from rest_framework.response import Response
from rest_framework import status


class ConversationsListView(ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = ViewPagination

    def get_queryset(self):
        if self.request.user:
            return Chat.get_user_chats(self.request.user)
        return []


class ChatRoomView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, chat_id, *args, **kwargs):
        try:
            chat = Chat.objects.get(id=chat_id)
        except Chat.DoesNotExist:
            return Response(
                {"message": "Chat not available for this mentorship."},
                status=status.HTTP_404_NOT_FOUND
            )
        messages = Message.objects.filter(chat=chat) if chat else []
        return render(request, 'conversation.html', {
            'chat_id': chat.id,
            'chat_name': chat.__str__(),
            'messages': messages
        })
