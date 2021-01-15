# Built in imports.
import json
# Third Party imports.
from channels.exceptions import DenyConnection
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync

# Django imports.
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import AnonymousUser

# DRF imports.
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed

# Local imports.
import pdb

class LiveScoreConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            # Pass auth token as a part of url.
            # token = self.scope.get('url_route', {}).get(
            #     'kwargs', {}).get('token', False)
            # # If no token specified, close the connection
          
            self.room_group_name = f'UFC'

            # if not token:
            #     raise DenyConnection("Token Invalid")
            # # Try to authenticate the token from DRF's Token model'
            # try:
            #     token = Token.objects.select_related('user').get(key=token)
            # except Token.DoesNotExist:
            #     raise DenyConnection("Token Invalid")

            # user = token.user

            # self.room_name = str(user.id)
            self.room_name = 'user'
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

    async def receive(self, text_data):
        print('====================')
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'live_score',
                'message': self.room_name,
            }
        )   

    async def live_score(self, event):
        print('event', event)
        try:
            # Here helper function fetches live score from DB.
            await self.send(text_data=json.dumps({
                'data': event['data']
            }))
        except Exception as err:
            print('live_score', err)

    # async def websocket_disconnect(self, message):
    #      # Leave room group
    #     await self.channel_layer.group_discard(
    #         self.room_group_name,
    #         self.channel_name
    #     )

    async def disconnect(self, close_code):
        print('close_code', close_code)
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

