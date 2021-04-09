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

from contest.commons import get_games_with_entry, main_contest

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
    def get_event_bouts(self, request, **kwarg):
        status = 200
        bouts = []
        try:
            bouts = BoutSerializer(Bout.objects.filter(event__id=request.data['id']), many=True).data
            for bout in bouts:
                bout['fighter1'] = FighterSerializer(Fighter.objects.get(id=bout['fighter1'])).data
                bout['fighter2'] = FighterSerializer(Fighter.objects.get(id=bout['fighter2'])).data
        except Exception as e:
            status = 400

        return Response(dict(bouts=bouts), status)

    @action(methods=['post'], detail=False)
    def get_latestevent(self, request, **kwarg):
        try:
            latest_event = Event.objects.latest_event()
            if latest_event:
                games = []
                if request.user.id:
                    game_id = int(request.data['game_id'])
                    entry_number = int(request.data['entry_number'])
                    try:
                        if game_id == -1:
                            cur_game = main_contest()
                        else:
                            cur_game = Game.objects.get(id=game_id)
                        my_entry = Entry.objects.all().filter(user_id=request.user.id, game_id=cur_game.id, entry_number=entry_number).first()
                    except:
                        pass
                    if cur_game and cur_game != -1:
                        latest_event = cur_game.event
                    bouts = BoutSerializer(cur_game.bouts, many=True).data
                    if not bouts:
                        bouts = BoutSerializer(Bout.objects.filter(event__id=latest_event.id), many=True).data
                    for bout in bouts:
                        bout['survivors'] = []
                        bout['fighter1'] = FighterSerializer(Fighter.objects.get(id=bout['fighter1'])).data
                        bout['fighter1']['division'] = bout['division']
                        bout['fighter2'] = FighterSerializer(Fighter.objects.get(id=bout['fighter2'])).data
                        bout['fighter2']['division'] = bout['division']
                    if my_entry:
                        latest_event = my_entry.event
                        for bout in bouts:
                            selected = Selection.objects.all().filter(entry_id=my_entry.id, bout_id=bout['id'])
                            if selected:
                                if selected[0].survivor1_id:
                                    bout['survivors'].append(selected[0].survivor1_id)
                                if selected[0].survivor2_id:
                                    bout['survivors'].append(selected[0].survivor2_id)

                    games = get_games_with_entry(latest_event, request.user.id)
                else:
                    games = get_games_with_entry(latest_event)
                return Response(dict(
                    bouts=bouts,
                    games=games,
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
