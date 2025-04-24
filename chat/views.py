from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from mentorship.serializers import UserSerializer
from chat.models import Message, Chat, User
from chat.pagination import ViewPagination
from django.contrib.auth.decorators import login_required


class ConversationsListView(ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = ViewPagination

    def get_queryset(self):
        if self.request.user:
            return Chat.get_user_chats(self.request.user)
        return []


@login_required
def chat_room_view(request, mentorship_id):
    chat = Chat.objects.filter(mentorship_id=mentorship_id).first()
    messages = Message.objects.filter(chat=chat) if chat else []

    return render(request, 'conversation.html', {
        'mentorship_id': mentorship_id,
        'chat': chat,
        'messages': messages
    })
