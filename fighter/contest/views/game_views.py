from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework_extensions.mixins import NestedViewSetMixin

from django.conf import settings

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

from contest.commons import load_my_games

import pdb

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
            event = Event.objects.latest_event()
            games = load_my_games(event, request.user.id)
        except Exception as err:
            print(err)
            status = 500

        return Response(dict(games=games), status)

    @action(methods=['get'], detail=False)
    def create_game(self, request, **kwarg):
        status = 200
        message = 'Successfully created'
        try:
            event = Event.objects.latest_event()
            if event:
                create_main_contest(event)
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
            if game.genre != 'free':
                if user.coins < game.buyin:
                    return Response(dict(message="You don't have enough coins."), 400)

                user.coins -= game.buyin
                user.save()

            game.joined_users.add(user)
            game.save()
        except Exception as err:
            print(err)
            status = 500
            message = 'Something went wrong.'

        return Response(dict(message=message), status)
