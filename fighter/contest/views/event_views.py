from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework_extensions.mixins import NestedViewSetMixin
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

import copy
from requests_oauthlib import OAuth1
from urllib.parse import urlencode
from django.conf import settings
import requests
from datetime import datetime

from django.contrib.auth.models import Group
from contest.decorators import paginate
from contest.models import (
    Event,
    Bout,
    Fighter,
    Selection,
    Entry,
    Game,
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
    GameSerializer,
	FighterSerializer,
    SelectionSerializer,
    EntrySerializer,
    ChatRoomSerializer,
    ChatFileSerializer,
    ChatMessageSerializer
)

import pdb

def show__latest_event():
    events = Event.objects.filter(status='upcoming')
    event = None
    if events:
        event = events.latest('-date')
    return event

class EventViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows events to be viewed or edited.
    """
    queryset = Event.objects.all().order_by('date')
    serializer_class = EventSerializer
    permission_classes = [permissions.AllowAny]
    # permission_classes = [permissions.IsAuthenticated]

    @action(methods=['post'], detail=False)
    def get_latestevent(self, request, **kwarg):
        try:
            events = Event.objects.all().filter(status='upcoming')
            if events:
                latest_event = events.latest('-date')
                bouts = Bout.objects.filter(event__id=latest_event.id)
                _bouts = BoutSerializer(bouts, many=True).data
                _bouts = sorted(_bouts, key = lambda _bout: _bout['id'])
                games = []
                fighters = []
                for bout in bouts:
                    fighters.append(FighterSerializer(bout.fighter1).data)
                    fighters.append(FighterSerializer(bout.fighter2).data)
                if request.user.id:
                    game_id = int(request.data['game_id'])
                    retry_number = int(request.data['retry_number'])
                    my_entry = None
                    cur_game = None
                    try:
                        if int(game_id) == -1:
                            my_entry = Entry.objects.all().get(user_id=request.user.id, event_id=latest_event.id, game__isnull=True)
                        else:
                            cur_game = Game.objects.get(id=game_id)
                            my_entry = Entry.objects.all().get(user_id=request.user.id, game_id=game_id, retry_number=retry_number)
                    except:
                        pass
                    if cur_game:
                        latest_event = cur_game.event
                    if my_entry:
                        latest_event = my_entry.event
                        bouts = Bout.objects.filter(event__id=latest_event.id)
                        _bouts = BoutSerializer(bouts, many=True).data
                        _bouts = sorted(_bouts, key = lambda _bout: _bout['id'])
                        for bout in _bouts:
                            selected = Selection.objects.all().filter(entry_id=my_entry.id, bout_id=bout['id'])
                            if selected:
                                bout['survivors'] = []
                                if selected[0].survivor1_id:
                                    bout['survivors'].append(selected[0].survivor1_id)
                                if selected[0].survivor2_id:
                                    bout['survivors'].append(selected[0].survivor2_id)

                    games = Game.objects.get_games(latest_event, request.user.id)
                else:
                    games = Game.objects.get_games(latest_event)
                return Response(dict(
                    bouts=_bouts,
                    games=games,
                    fighters=fighters,
                    event=EventSerializer(latest_event).data
                ))
            else:
                return Response(dict(
                    bouts=[],
                    games=[],
                    event=None
                ))
        except Exception as err:
            print(err)
            return Response(dict(
                    bouts=[],
                    event=None,
                    games=[],
                    message=str(err)
                ), status=500)
