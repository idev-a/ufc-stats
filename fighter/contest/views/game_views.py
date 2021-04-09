from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework_extensions.mixins import NestedViewSetMixin

from django.conf import settings
from datetime import datetime

from contest.models import (
    Event,
    Bout,
    Fighter,
    Selection,
    Entry,
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

from contest.commons import load_my_games, load_own_games, build_games

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
        latest_event = {}
        upcoming_events = []
        bouts = []
        status = 200
        try:
            event = Event.objects.latest_event()
            latest_event = EventSerializer(event).data
            bouts = BoutSerializer(Bout.objects.filter(event__id=latest_event['id']), many=True).data
            for bout in bouts:
                bout['fighter1'] = FighterSerializer(Fighter.objects.get(id=bout['fighter1'])).data
                bout['fighter2'] = FighterSerializer(Fighter.objects.get(id=bout['fighter2'])).data
            upcoming_events = EventSerializer(Event.objects.filter(status='upcoming').order_by('-date'), many=True).data
            games = load_my_games(event, request.user.id)
        except Exception as err:
            print(err)
            status = 500

        return Response(dict(games=games, latest_event=latest_event, upcoming_events=upcoming_events, bouts=bouts), status)

    @action(methods=['get'], detail=False)
    def load_own_games(self, request, **kwarg):
        my_own_games = []
        status = 200
        message = 'Successfully done.'
        try:
            if not request.user:
                raise Exception()
            my_own_games = load_own_games(request.user.id)
        except Exception as err:
            print(err)
            message = 'Something went wrong.'
            status = 500

        return Response(dict(my_own_games=my_own_games), status)

    @action(methods=['post'], detail=False)
    def delete_game(self, request, **kwarg):
        status = 200
        message = 'Successfully done'
        try:
            if not request.user or not request.data['game_id']:
                raise Exception()
            Game.objects.get(id=request.data['game_id']).delete()
        except Exception as err:
            print(err)
            status = 500
            message = 'Something went wrong.'

        return Response(dict(message=message), status)

    @action(methods=['post'], detail=False)
    def create_game(self, request, **kwarg):
        status = 200
        message = 'Successfully created'
        games = []
        try:
            if not request.user:
                raise Exception()
            data = request.data
            data['owner'] = request.user.id
            game_serializer = GameSerializer(data=data)
            if game_serializer.is_valid():
                game = game_serializer.save()
                build_games(games, [game], None, request.user.id)
            else:
                raise Exception()
        except Exception as err:
            print(err)
            status = 500
            message = 'Something went wrong.'

        return Response(dict(message=message, game=games[-1]), status)

    @action(methods=['post'], detail=False)
    def update_game(self, request, **kwarg):
        status = 200
        message = 'Successfully updated'
        try:
            if not request.user:
                raise Exception()
            data = request.data
            data['owner'] = request.user.id
            game = Game.objects.get(id=data['id'])
            if game:
                game.name = data['name']
                game.instructions = data['instructions']
                game.rules_set = data['rules_set']
                game.summary = data['summary']
                game.multientry = data['multientry']
                game.buyin = data['buyin']
                game.added_prizepool = data['added_prizepool']
                game.save()
            else:
                raise Exception()
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
            if not request.user:
                raise Exception()
            game = Game.objects.get(pk=request.data['game_id'])
            if game.genre != 'free':
                if request.user.coins < game.buyin:
                    return Response(dict(message="You don't have enough coins."), 400)
                
                # deduct user's coins by buyin
                request.user.coins -= game.buyin
                request.user.save()

            # create new entry with the new entry_number if possible
            entries = Entry.objects.filter(game=game.id).filter(user=request.user.id).order_by('entry_number')
            entry_number = 0
            if not entries:
                entry_number = 1
            if entries.count() < game.multientry:
                for x, entry in enumerate(entries):
                    if entry.entry_number != x+1:
                        # Just in case the entry with the middle number was eliminated in My Teams page
                        entry_number = x + 1
                        break
                # last position + 1
                if not entry_number:
                    entry_number = entries.count() + 1

            if entry_number and entries.count() < game.entry_limit:
                new_entry = Entry(event=game.event, game=game, user=request.user, entry_number=entry_number)
                new_entry.save()

                # add user to joined_users list in the game
                game.joined_users.add(request.user)
                game.save()

        except Exception as err:
            print(err)
            status = 500
            message = 'Something went wrong.'

        return Response(dict(message=message, status=status, entry_number=entry_number), status)

