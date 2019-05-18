import json
import logging
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.core.cache import cache

# from chat.libs.websocket_handler import connect, receive, disconnect


logger = logging.getLogger(__name__)


class CustomConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        # Join group group_add('group_name', 'channel_name')
        await self.channel_layer.group_add(
            'lobby',
            self.channel_name
        )
        username = self.scope.get('username')
        await self.accept()
        await self.group_send(f'{username} join the room.')

    async def disconnect(self, close_code):
        # Leave group group_discard('group_name', 'channel_name')
        await self.channel_layer.group_discard(
            'lobby',
            self.channel_name
        )
        username = self.scope.get('username')
        await self.group_send(f'{username} left the room.')

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        username = self.scope.get('username')
        message = username + ':::::: ' + text_data_json['message']
        # Send message to room group
        await self.group_send(message)

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))

    async def personal_message(self, event):
        message = event['haha']
        await self.send(text_data=json.dumps({
            'personal_message': message
        }))

    async def group_send(self, msg, group='lobby', type_='chat_message'):
        # group_send('group_name', {'type': type, **kwargs})
        await self.channel_layer.group_send(
            group,
            {
                'type': type_,
                'message': msg
            }
        )
