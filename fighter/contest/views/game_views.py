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

from contest.decorators import paginate
from contest.models import (
    Event,
    Bout,
    Fighter,
    Selection,
    Entry,
    CustomUser,
    Game
)
from contest.serializers import (
    UserSerializer,
    GroupSerializer,
    EventSerializer,
    BoutSerializer,
    FighterSerializer,
    SelectionSerializer,
    EntrySerializer,
    GameSerializer
)

import pdb

def show__games():
    for _ in Game.objects.all():
        yield dict(
            id=_.id,
            name=_.name,
            event=EventSerializer(_.event).data,
            type_of_registration=_.type_of_registration,
            joined_users=UserSerializer(_.joined_users.all(), many=True).data,
            entrants=UserSerializer(_.entrants.all(), many=True).data,
            instructions=_.instructions,
            rules_set=_.rules_set,
            date=_.date,
            action=_.action
        )


class GameViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows entries to be viewed or edited.
    """
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [permissions.AllowAny]
    # permission_classes = [permissions.IsAuthenticated]

    @action(methods=['get'], detail=False)
    def load_games(self, request, **kwarg):
        games = []
        status = 200
        try:
            games = [_ for _ in show__games()]
        except Exception as err:
            status = 500

        return Response(dict(games=games), status)

    @action(methods=['post'], detail=False)
    def create_game(self, request, **kwarg):
        status = 200
        message = 'Successfully created'
        try:
            pass
        except Exception as err:
            print(err)
            status = 500
            message = 'Something went wrong.'

        return Response(dict(message=message), status)

    @action(methods=['post'], detail=False)
    def join_game(self, request, **kwarg):
        status = 200
        message = 'Successfully Joined'
        try:
            user = CustomUser.objects.get(pk=request.data['user_id'])
            game = Game.objects.get(pk=request.data['game_id'])
            game.joined_users.add(user)
            game.save()
        except Exception as err:
            print(err)
            status = 500
            message = 'Something went wrong.'

        return Response(dict(message=message), status)
