import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

from .models import Room, Message
from apps.users.models import User

_logger = logging.getLogger('main')


class RoomConsumer(AsyncWebsocketConsumer):
    """consumer that will handle the conections from the room"""

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['pk']
        self.room_group_name = 'chat_%s' % self.room_name
        _logger.info(
            f"client with ip [{self.scope['client'][0]}]"
            f" connected to {self.room_group_name}"
        )
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )
        await self.accept()

    async def disconnect(self, code):
        _logger.info(
            f"client with ip [{self.scope['client'][0]}] "
            f"disconnected from {self.room_group_name}"
        )
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )

    # receive messege from room
    async def receive(self, text_data):
        data = json.loads(text_data)
        _logger.info(
            f'{self.room_group_name}: '
            f'message received from {data["useremail"]}: "{data["message"]}"'
        )

        _logger.info(f'storing message "{data["message"]}" in the database')
        await self.save_message(**data)

        _logger.info(
            f'broadcasting message: "{data["message"]}" '
            f'to room {self.room_group_name}',
        )
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'room_message',
                'message': data['message'],
                'useremail': data['useremail'],
            },
        )

    async def room_message(self, event):
        data = {'message': event['message'], 'useremail': event['useremail']}
        # Send message to WebSocket
        await self.send(text_data=json.dumps(data))

    @sync_to_async
    def save_message(self, useremail, room_id, message):
        user = User.objects.get(email=useremail)
        room = Room.objects.get(pk=room_id)
        message = Message.objects.create(
            sender=user,
            room=room,
            content=message,
        )
