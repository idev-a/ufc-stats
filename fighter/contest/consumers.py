# Built in imports.
import json
# Third Party imports.
from channels.exceptions import DenyConnection
from channels.generic.websocket import AsyncWebsocketConsumer, AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async

# Django imports.
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import AnonymousUser

# DRF imports.
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed

import pdb
# Local imports.

from contest.models import (
    ChatMessage
)

from contest.serializers import (
    UserSerializer,
    GroupSerializer,
    EventSerializer,
    BoutSerializer,
    FighterSerializer,
    SelectionSerializer,
    EntrySerializer,
    ChatRoomSerializer,
    ChatFileSerializer,
    ChatMessageSerializer
)

class LiveScoreConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        try:
            # Pass auth token as a part of url.
            # token = self.scope.get('url_route', {}).get(
            #     'kwargs', {}).get('token', False)
            # # If no token specified, close the connection

            # if not token:
            #     raise DenyConnection("Token Invalid")
            # # Try to authenticate the token from DRF's Token model'
            # try:
            #     token = Token.objects.select_related('user').get(key=token)
            # except Token.DoesNotExist:
            #     raise DenyConnection("Token Invalid")

            # user = token.user

            # self.room_name = str(user.id)
            self.room_name = 'chat'
            self.room_group_name = f'UFC_{self.room_name}'
            # if self.scope['user'] == AnonymousUser():
            #     raise DenyConnection("Invalid User")
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            # If invalid game id then deny the connection.
            # try:
            #     self.game = Game.objects.get(pk=self.room_name)
            # except ObjectDoesNotExist:
            #     raise DenyConnection("Invalid Game Id")
            await self.accept()
        except Exception as e:
            raise DenyConnection("Invalid")

    async def receive_json(self, data):
        if data['commands']:
            await self.commands[data['commands']](self, data['data'])
       
    async def live_score(self, event):
        print(event)
        try:
            # Here helper function fetches live score from DB.
            await self.send_json (event['data'])
        except Exception as err:
            print('live_score', err)

    async def chat_message(self, event):
        await self.send_json({
            'type': 'chat_message',
            'commands': event['commands'],
            'messages': event['messages']
        })

    async def disconnect(self, close_code):
        print('close_code', close_code)
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    @database_sync_to_async
    def fetch_messages(self, data):
        res = ChatMessage.objects.all().order_by('-timestamp').filter(room_id=data['room_id']).filter(pk__gt=data['idx'])
        messages = ChatMessageSerializer(res, many=True).data
        
        self.format_messages(messages)
        
        self.send_json({
            'type': 'chat_message',
            'commands': 'fetch_messages',
            'messages': messages
        })

    async def new_message(self, data):
        messages = await self.action_new_message(data)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'messages': messages,
                'commands': 'new_message',
            }
        )

    async def edit_message(self, data):
        messages = await self.action_edit_message(data)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'messages': messages,
                'commands': 'edit_message',
            }
        )

    async def delete_message(self, data):
        messages =  await self.action_delete_message(data)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'messages': messages,
                'commands': 'delete_message',
            }
        )

    @database_sync_to_async
    def action_new_message(self, data):
        chat_serializer = ChatMessageSerializer(data=data)
        chat_serializer.is_valid()
        message = chat_serializer.save()
        _message = chat_serializer.data
        if message.reply_message:
            reply_message = ChatMessage.objects.get(pk=message.reply_message_id)
            _message['reply_message'] = ChatMessageSerializer(reply_message).data
        messages = [_message]
        self.format_messages(messages)
        return messages

    @database_sync_to_async
    def action_delete_message(self, data):
        message = ChatMessage.objects.all().filter(pk=data['id']).first()
        chat_serializer = ChatMessageSerializer(message, data=data)
        chat_serializer.is_valid()
        message = chat_serializer.save()
        messages = [chat_serializer.data]
        self.format_messages(messages)
        return messages

    @database_sync_to_async
    def action_edit_message(self, data):
        message = ChatMessage.objects.all().filter(pk=data['id']).first()
        chat_serializer = ChatMessageSerializer(message, data=data)
        chat_serializer.is_valid()
        message = chat_serializer.save()
        messages = [chat_serializer.data]
        self.format_messages(messages)
        return messages

    def format_messages(self, messages):
        for _ in messages:
            _['_id'] = _['id']
            _['sender_id'] = _['sender']

    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message,
        'edit_message': edit_message,
        'delete_message': delete_message,
    }