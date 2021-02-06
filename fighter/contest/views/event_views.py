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

import pdb

class EventViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows events to be viewed or edited.
    """
    queryset = Event.objects.all().order_by('date')
    serializer_class = EventSerializer
    permission_classes = [permissions.AllowAny]
    # permission_classes = [permissions.IsAuthenticated]

    def _selection(self, selections, bout):
        selected = None
        for selection in selections:
            if selection.bout_id == bout['id']:
                selected = selection
                break

        return selected

    @action(methods=['get'], detail=False)
    def get_latestevent(self, request, **kwarg):
        try:
            events = Event.objects.all().filter(status='upcoming')
            if events:
                latest_event = events.latest('-date')
                bouts = Bout.objects.filter(event__id=latest_event.id)
                _bouts = BoutSerializer(bouts, many=True).data
                _bouts = sorted(_bouts, key = lambda _bout: _bout['id'])
                if request.user.id:
                    selections = Selection.objects.all().filter(entry__user_id=request.user.id).filter(entry__event_id=latest_event.id)
                    for bout in _bouts:
                        selected = self._selection(selections, bout)
                        if selected:
                            bout['survivors'] = []
                            if selected.survivor1_id:
                                bout['survivors'].append(selected.survivor1_id)
                            if selected.survivor2_id:
                                bout['survivors'].append(selected.survivor2_id)

                return Response(dict(
                    bouts=_bouts,
                    event=EventSerializer(latest_event).data
                ))
            else:
                return Response(dict(
                    bouts=[],
                    event=None
                ))
        except Exception as err:
            return Response(dict(
                    bouts=[],
                    event=None,
                    message=str(err)
                ), status=500)
