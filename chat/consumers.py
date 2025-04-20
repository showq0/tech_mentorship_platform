from channels.generic.websocket import AsyncWebsocketConsumer
import json


class MyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send(text_data=json.dumps({"message": "ASGI is configured correctly"}))

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        await self.send(text_data=json.dumps({"echo": text_data}))
