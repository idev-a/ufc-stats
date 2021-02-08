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

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = CustomUser.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes_by_action = {
        'create': [permissions.IsAuthenticated],
        'list': [permissions.IsAuthenticated],
        'get_all': [permissions.IsAuthenticated],
        'request_referral_url': [permissions.AllowAny],
    }

    @action(methods=['post'], detail=False)
    def get_all(self, request, **kwarg):
        users = []
        status = 200
        try:
            res = CustomUser.objects.all().filter(pk__in=request.data)
            serializer_context = {
                'request': request._request,
            }
            users = UserSerializer(res, many=True, context=serializer_context).data
            for _ in users:
                _['_id'] = _['id']
        except Exception as err:
            status = 500

        return Response(dict(users=users), status)

    @action(methods=['post'], detail=False)
    def request_referral_url(self, request, **kwarg):
        status = 200
        url = ''
        try:
            user_id = request.data.get('id')
        except Exception as err:
            status = 403

        return Response(dict(url=url), status)

    @action(methods=['get'], detail=False)
    def get_profile(self, request, **kwarg):
        status = 200
        data = {'contest_history': []}
        try:
            data['total_contests'] = Entry.objects.filter(user_id=request.user.id).count()
            total_wins = Entry.objects.filter(user_id=request.user.id, ranking=1).count()
            data['total_wins'] = "{:5.1f}".format(total_wins/data['total_contests'] * 100) 
            # contest history
            entries = Entry.objects.filter(user_id=request.user.id)
            for _ in entries:
                event = Event.objects.get(pk=_.event_id)
                _event = EventSerializer(event).data
                _entry = EntrySerializer(_).data
                data['contest_history'].append(dict(
                    id= _entry['id'],
                    event=_event['name'],
                    date=_event['date'],
                    ranking=_.ranking,
                    last_edited=_entry['last_edited']
                ))
        except Exception as err:
            status = 500

        return Response(data, status)

