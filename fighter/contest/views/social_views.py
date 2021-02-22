from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework_extensions.mixins import NestedViewSetMixin
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

import copy
from requests_oauthlib import OAuth1
from urllib.parse import urlencode
from django.conf import settings
import requests
from datetime import datetime
import base64
import hashlib
import hmac
import json
import re
import shlex
import logging

from django.contrib.auth.models import Group
from contest.decorators import paginate
from contest.models import (
    Event,
    Bout,
    Fighter,
    Selection,
    Entry,
    CustomUser,
    ChatRoom,
    ChatFile, 
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

from contest.views import (
    event_views,
)

from allauth.socialaccount.providers.twitter.views import TwitterOAuthAdapter
from rest_auth.registration.views import SocialLoginView
from rest_auth.social_serializers import TwitterLoginSerializer
from contest.myconfig import create_api
from decouple import config

import pdb

logger = logging.getLogger(__name__)

START_KEYWORD = '@jason5001001'

class CustomTwitterLoginSerializer(TwitterLoginSerializer):

    def validate(self, attrs):
        _attrs = super().validate(attrs)

        user = _attrs['user']
        user.displayname = user.username
        _attrs['user'] = user
        user.save()
        return _attrs

# Social
class TwitterLogin(SocialLoginView):
    serializer_class = CustomTwitterLoginSerializer
    adapter_class = TwitterOAuthAdapter


class TwitterAuthRedirectEndpoint(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        try:
            oauth = OAuth1(
                config('TWITTER_CONSUMER_KEY'), 
                client_secret=config('TWITTER_CONSUMER_SECRET')
            )
            #Step one: obtaining request token
            request_token_url = "https://api.twitter.com/oauth/request_token"
            data = urlencode({
                "oauth_callback": config('TWITTER_AUTH_CALLBACK_URL')
            })
            response = requests.post(request_token_url, auth=oauth, data=data)
            response.raise_for_status()
            response_split = response.text.split("&")
            oauth_token = response_split[0].split("=")[1]
            oauth_token_secret = response_split[1].split("=")[1]  

            #Step two: redirecting user to Twitter
            twitter_redirect_url = (f"https://api.twitter.com/oauth/authenticate?oauth_token={oauth_token}")
            return Response(dict(twitter_redirect_url=twitter_redirect_url), status=200)
        except ConnectionError:
            return Response(dict(message=["You have no internet connection"]), status=403)
        except Exception as err:
            print(err)
            return Response(dict(message=["Something went wrong.Try again."]), status=403)


class TwitterCallbackEndpoint(APIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, request, *args, **kwargs):
        try:
            oauth_token = request.query_params.get("oauth_token")
            oauth_verifier = request.query_params.get("oauth_verifier")
            oauth = OAuth1(
                config('TWITTER_CONSUMER_KEY'),
                client_secret=config('TWITTER_CONSUMER_SECRET'),
                resource_owner_key=oauth_token,
                verifier=oauth_verifier,
            )
            res = requests.post(
                f"https://api.twitter.com/oauth/access_token", auth=oauth
            )
            res_split = res.text.split("&")
            oauth_token = res_split[0].split("=")[1]
            oauth_secret = res_split[1].split("=")[1]

            formdata = {
                'access_token': oauth_token,
                'token_secret': oauth_secret
            }
            url = f"{request.scheme}://{request.get_host()}/auth/twitter/"
            res = requests.post(url, data=formdata).json()
            return Response(dict(key=res['key']))
        except ConnectionError:
            return Response(dict(message=["You have no internet connection"]), status=403)
        except Exception as err:
            print(err)
            return Response(dict(message=["Something went wrong.Try again."]), status=403)

class TwitterWebhookEndpoint(APIView):
    permission_classes = [permissions.AllowAny]

    def __init__(self):
        self.tweepy_api = create_api()

    def reply(self, text, id):
        self.tweepy_api.update_status(
            status=text,
            in_reply_to_status_id=id,
        )

    def upload_photo(self, text, id, path):
        img = self.tweepy_api.media_upload(path)
        self.tweepy_api.send_direct_message(id, text, attachment_type='media', attachment_media_id=img.media_id)

    def create_game(self, reply_id, owner_id, args, event=None, type='private'):
        owner = None
        message = 'Successfully created.'
        try:
            owner = CustomUser.objects.get(username=owner_id)
        except:
            message = "You are not allowed to create a game. Please register account first."
            self.reply(message, reply_id)
            return

        entrants = []
        for idx in range(len(args)):
            if args[idx] == '-u':
                entrants = args[idx+1]

        game = Game.objects.create(owner=owner)
        game.type_of_registration = type
        if not even:
            # choose latest event
            game.event = show__latest_event()
        else:
            game.event = event

        # instructions, rules_set
        non_users = []
        for id in entrants:
            try:
                user = CustomUser.objects.get(username=id)
                game.entrants.add(user)
            except:
                non_users.append(id)

        if non_users:
            message += "The following users didn't have accounts yet. " + ','.join(non_users)

        self.reply(message, reply_id)

    def manage_shows(self, reply_id, block):
        first_command = block.split(' ')[0]
        if first_command == 'show__all_commands':
            self.reply('show__latest_event', reply_id)

        elif first_command == 'show__latest_event':
            event = event_views.show__latest_event()
            self.reply(event.__str__(), reply_id)
        elif first_command == 'show__games':
            image_path = f"{reply_id}.png"
            html2png(image_path)
            tweet_text = 'The below shows top games'
            status = api.update_with_media(image_path, tweet_text, in_reply_to_status_id='1362837934567616515')
    
    def manage_creates(self, reply_id, owner_id, block):
        first_command = block.split(' ')[0]
        if first_command == 'create_private_game':
            args = shlex.split(' '.join(block.split(' ')[1:].strip()))
            print(args)
            self.create_game(reply_id, owner_id, args)

    def get(self, request, *args, **kwargs):
        try:
            key_bytes= config('TWITTER_BOT_CONSUMER_SECRET').encode('utf-8') # Commonly 'latin-1' or 'utf-8'
            data_bytes = request.query_params.get('crc_token').encode('utf8') # Assumes `data` is also a string.
            # creates HMAC SHA-256 hash from incomming token and your consumer secret
            sha256_hash_digest = hmac.new(key_bytes, msg=data_bytes, digestmod=hashlib.sha256).digest()

            # construct response data with base64 encoded hash
            response = {
                'response_token': 'sha256=' + base64.b64encode(sha256_hash_digest).decode('utf-8')
            }

            # returns properly formatted json response
            return Response(response)
        except ConnectionError:
            return Response(dict(message=["You have no internet connection"]), status=403)
        except Exception as err:
            logger.error(str(err))
            return Response(dict(message=["Something went wrong.Try again."]), status=403)

    def post(self, request, format=None):
        # request.data
        '''
            check @fightquake and respond based upon command
        '''
        for tweet in request.data['tweet_create_events']:
            if tweet:
                try:
                    commands_block = tweet['text'].split(START_KEYWORD)[1].strip()
                    first_command = commands_block.split(' ')[0]
                    reply_id = tweet['id'] or tweet['in_reply_to_status_id']
                    if first_command.startswith('show__'):
                        self.manage_shows(reply_id, commands_block)

                    if first_command.startswith('create__'):
                        self.manage_creates(reply_id, tweet['user']['screen_name'], commands_block)
                except Exception as err:
                    logger.error(str(err))
