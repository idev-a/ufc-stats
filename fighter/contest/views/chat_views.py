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

from contest.views.common_views import StandardResultsSetPagination

class ChatRoomViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows chat rooms to be viewed or edited.
    """
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer
    permission_classes = [permissions.AllowAny]
    # permission_classes = [permissions.IsAuthenticated]

    @action(methods=['get'], detail=False)
    def get_all(self, request, **kwarg):
        # limit by roomPerPage
        idx = request.query_params.get('idx', 0)
        res = ChatRoom.objects.all().order_by('-last_updated').filter(id__gt=idx)
        rooms = ChatRoomSerializer(res, many=True).data
        users = CustomUser.objects.all()
        for _ in rooms:
            _['_id'] = _['id']
            for user in users:
                if user.id not in _['users']:
                    _['users'].append(user.id)

        return Response(dict(rooms=rooms))

class ChatFileViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows chat file to be viewed or edited.
    """
    queryset = ChatFile.objects.all()
    serializer_class = ChatFileSerializer
    permission_classes = [permissions.AllowAny]
    # permission_classes = [permissions.IsAuthenticated]

class ChatMessageViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows entries to be viewed or edited.
    """
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = StandardResultsSetPagination
    # permission_classes = [permissions.IsAuthenticated]

    def format_message(self, data):
        messages = []
        for _ in data:
            _['_id'] = _['id']
            _['sender_id'] = _['sender']
            messages.append(_)
        return messages

    @action(methods=['get'], detail=False)
    def get_by_room(self, request, **kwarg):
        messages = []
        return Response(dict(messages=messages))

    @action(methods=['get'], detail=False)
    def get_latest(self, request, **kwarg):
        room_id = request.query_params.get('room_id')
        message = ChatMessage.objects.all().filter(room_id=room_id)
        messages = []
        if message:
            messages = [self.get_serializer(message.latest('timestamp')).data]
        messages = self.format_message(messages)

        return Response(dict(messages=messages))


    @action(methods=['get'], detail=False)
    def get_all(self, request, **kwarg):
        # limit by messagePerPage
        room_id = request.query_params.get('room_id')
        idx = int(request.query_params.get('idx', '0'))
        message = ChatMessage.objects.all().filter(room_id=room_id).order_by('-timestamp', 'id')
        page = self.paginate_queryset(message)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            messages = self.format_message(serializer.data)
            return self.get_paginated_response(messages)
        
        serializer = self.get_serializer(message, many=True)
        messages = self.format_message(serializer.data)
        return Response(dict(results=messages))