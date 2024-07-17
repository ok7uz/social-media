import json
from channels.generic.websocket import AsyncWebsocketConsumer


class NotificationConsumer(AsyncWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None
        self.group_name = None

    async def connect(self):
        print(self.channel_layer.groups)
        self.user = self.scope['user']
        self.group_name = f'user_{self.user.id}'
        print(self.channel_layer, self.user)
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        print(self.channel_layer)

    async def send_notification(self, event):
        print(await self.send(text_data=json.dumps({'message': event['text']})))
