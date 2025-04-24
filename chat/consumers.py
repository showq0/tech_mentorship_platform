import json
from channels.generic.websocket import AsyncWebsocketConsumer
from chat.models import Message
from channels.db import database_sync_to_async


class MessagesConsumer(AsyncWebsocketConsumer):
    chat_id = None

    @database_sync_to_async
    def save_message(self, sender_id, content, chat_id):
        Message.objects.create(sender_id=sender_id, content=content, chat_id=chat_id)

    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.chat_room = f'chat_id{self.chat_id}'

        # Join chat group  is a collection of channels
        await self.channel_layer.group_add(
            self.chat_room,
            self.channel_name
        )

        await self.accept()

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        sender_name = data['sender_name']
        sender_id = data['sender_id']

        await self.save_message(sender_id, message, self.chat_id)

        await self.channel_layer.group_send(
            self.chat_room,
            {
                'type': 'chat_message',  # map to send method
                'message': message,
                'sender_name': sender_name
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender_name = event['sender_name']

        await self.send(text_data=json.dumps({
            'message': message,
            'sender_name': sender_name
        }))
