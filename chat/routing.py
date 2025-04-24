from django.urls import re_path
from chat.consumers import MessagesConsumer

websocket_urlpatterns = [
    re_path(r'ws/messages/(?P<mentorship_id>\d+)/$', MessagesConsumer.as_asgi()),
]