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

import pdb

def show__games(user_id):
    events = Event.objects.all().filter(status='upcoming')
    if events:
        event = events.latest('-date')
        yield dict(
            id=-1,
            name='Main Contest',
            event=EventSerializer(event).data,
            type_of_registration='public',
            date=event.date,
            joined_users=None,
            entrants=None,
            genre='free',
            buyin=0,
            added_prizepool=0,
            prize=0,
            action=event.action,
            re_entry=False,
            multientry=1
        )
    if user_id:
        for _ in Game.objects.filter(entrants__pk=user_id).filter(event__action=''):
            yield dict(
                id=_.id,
                name=_.name,
                event=EventSerializer(_.event).data,
                type_of_registration=_.type_of_registration,
                genre=_.genre,
                buyin=_.buyin,
                prize=_.prize,
                added_prizepool=_.added_prizepool,
                joined_users=UserSerializer(_.joined_users.all(), many=True).data,
                entrants=UserSerializer(_.entrants.all(), many=True).data,
                instructions=_.instructions,
                summary=_.summary,
                rules_set=_.rules_set,
                date=_.date,
                action=_.action,
                re_entry=_.re_entry,
                multientry=_.multientry
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
            games = list(show__games(request.user.id))
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
