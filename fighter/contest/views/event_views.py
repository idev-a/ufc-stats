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

from contest.commons import get_games

import pdb

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
            latest_event = Event.objects.latest_event()
            if latest_event:
                bouts = Bout.objects.filter(event__id=latest_event.id)
                _bouts = BoutSerializer(bouts, many=True).data
                _bouts = sorted(_bouts, key = lambda _bout: _bout['id'])
                games = []
                fighters = []
                for bout in _bouts:
                    bout['survivors'] = []
                for bout in bouts:
                    fighters.append(FighterSerializer(bout.fighter1).data)
                    fighters.append(FighterSerializer(bout.fighter2).data)
                if request.user.id:
                    game_id = int(request.data['game_id'])
                    entry_number = int(request.data['entry_number'])
                    my_entry = None
                    cur_game = None
                    try:
                        if game_id == -1:
                            my_entry = Entry.objects.all().get(user_id=request.user.id, event_id=latest_event.id, game__isnull=True)
                        else:
                            cur_game = Game.objects.get(id=game_id)
                            my_entry = Entry.objects.all().filter(user_id=request.user.id, game_id=game_id, entry_number=entry_number).first()
                    except:
                        pass
                    if cur_game:
                        latest_event = cur_game.event
                    if my_entry:
                        latest_event = my_entry.event
                        for bout in _bouts:
                            selected = Selection.objects.all().filter(entry_id=my_entry.id, bout_id=bout['id'])
                            bout['survivors'] = []
                            if selected:
                                if selected[0].survivor1_id:
                                    bout['survivors'].append(selected[0].survivor1_id)
                                if selected[0].survivor2_id:
                                    bout['survivors'].append(selected[0].survivor2_id)

                    games = get_games(latest_event, request.user.id)
                else:
                    games = get_games(latest_event)
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
