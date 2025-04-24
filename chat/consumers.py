import json
from channels.generic.websocket import AsyncWebsocketConsumer


class MessagesConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.mentorship_id = self.scope['url_route']['kwargs']['mentorship_id']
        self.chat_room = f'mentorship_{self.mentorship_id}'

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

        await self.channel_layer.group_send(
            self.chat_room,
            {
                'type': 'chat_message', # map to send method
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