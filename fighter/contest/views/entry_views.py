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
import logging

from contest.decorators import paginate
from contest.models import (
    Event,
    Bout,
    Fighter,
    Selection,
    Entry,
    Game,
    CustomUser,
)
from contest.serializers import (
    UserSerializer,
    GroupSerializer,
    EventSerializer,
    GameSerializer,
    BoutSerializer,
    FighterSerializer,
    SelectionSerializer,
    EntrySerializer,
)

import pdb
logger = logging.getLogger(__name__)

def _exist(item, arr):
    is_exist = False
    for _item in arr:
        if _item['id'] == item['id']:
            is_exist = True
            break

    return is_exist

def _count_entries(fighter_id, selections):
    survivor1s = []
    for selection in selections:
        if selection.survivor1 and selection.survivor1.id == fighter_id:
            survivor1s.append([selection.survivor1.name, f"{selection.entry.user.displayname}"] ) 
         
    survivor2s = []
    for selection in selections:
        if selection.survivor2 and selection.survivor2.id == fighter_id:
            survivor2s.append([selection.survivor2.name, f"{selection.entry.user.displayname}"]) 
    return survivor1s + survivor2s

def _calc_suv_win_loss(survivor1, survivor2, winner, loser):
    wins = 0
    losses = 0
    if survivor1.get('id') == winner.get('id') or survivor2.get('id') == winner.get('id'):
        wins += 1
    if survivor1.get('id') == loser.get('id') or survivor2.get('id') == loser.get('id'):
        losses += 1

    return wins, losses

def update_rank(event_id):
    selections = Selection.objects.filter(entry__event_id=event_id)
    entry_views = get_entry_views(selections)
    status = 200
    try:
        for _ in entry_views:
            entry = get_object_or_404(Entry, pk=_['id'])
            entry.rank = _['rank']
            entry.save()
    except Entry.DoesNotExist:
        status = 404

    return Response(dict(status=status))

def get_games(latest_event, game_id, user_id):
    games = [{ 'header': 'Single' }]
    games.append(dict(
        event_id=latest_event.id,
        name=latest_event.name,
        group='Single',
        date=latest_event.date,
        value=-1,
        game_id=-1,
        action=latest_event.action
    ))
    multi_games = Game.objects.filter(joined_users__pk=user_id)
    if multi_games:
        games.append({ 'header': 'Multiple' })
        for _ in multi_games:
            games.append(dict(
                name=_.name,
                group='Multiple',
                date=_.date,
                value=_.id,
                game_id=_.id,
                action=_.action,
                event_id=_.event.id
            ))

    return games

def get_entry_views(selections):
    score = {}
    default_score = {
        'id': '',
        'game_id': -1,
        'entry': '',
        'method': '', 
        'survived': 0,
        'wins': 0,
        'losses': 0,
        'dead': 0,
        'remainings': 0,
        'fighters': [],
        'winners': [],
        'losers': [],
        'died': []
    }
    for selection in selections:
        # if selection.survivor1_id == None and selection.survivor2_id == None:
        #     continue
        username_id = f'{selection.entry.id}'
        bout = selection.bout
        method = bout.method

        winner_id = bout.winner and bout.winner.id # winner from bout
        score[username_id] = score.get(username_id, copy.deepcopy(default_score))
        score[username_id]['id'] = username_id
        score[username_id]['game_id'] = -1
        if selection.entry.game and selection.entry.game.id:
            score[username_id]['game_id'] = selection.entry.game.id
        score[username_id]['entry'] = selection.entry.user.displayname
        score[username_id]['user_id'] = selection.entry.user.id
        score[username_id]['last_edited'] = selection.entry.last_edited.timestamp()

        # Get winner and loser
        winner = {}
        if bout.winner:
            winner = { 'id': bout.winner.id, 'name': bout.winner.name }
        loser = {}
        if bout.loser:
            loser = { 'id': bout.loser.id, 'name': bout.loser.name }

        survivor1 = {}
        if selection.survivor1:
            _s1 = selection.survivor1
            survivor1 = {
                'id': _s1.id,
                'name': _s1.name,
                'win': _s1.id == winner.get('id'),
                'lose': _s1.id == loser.get('id'),
                'draw': bout.status == 'drawn',
                'entry_cnt': len(_count_entries(_s1 and _s1.id, selections))
            }
        survivor2 = {}
        if selection.survivor2:
            _s2 = selection.survivor2
            survivor2 = {
                'id': _s2.id,
                'name': _s2.name,
                'win': _s2.id == winner.get('id'),
                'lose': _s2.id == loser.get('id'),
                'draw': bout.status == 'drawn',
                'entry_cnt': len(_count_entries(_s2 and _s2.id, selections))  
            }

        if 'DEC' not in bout.method:
            if survivor1 and survivor1.get('id') == loser.get('id'):
                survivor1['died'] = True
            if survivor2 and survivor2.get('id') == loser.get('id'):
                survivor2['died'] = True

            if survivor1.get('died', False) or survivor2.get('died', False):
                score[username_id]['died'].append(loser)

        score[username_id]['method'] = method
        if survivor1:
            score[username_id]['fighters'].append(survivor1)
        if survivor2:
            score[username_id]['fighters'].append(survivor2)
        score[username_id]['winners'].append(winner)
        score[username_id]['losers'].append(loser)
        
        # remainings
        if bout.status == 'started' or bout.status == '':
            if selection.survivor1_id != None:
                score[username_id]['remainings'] += 1
            if selection.survivor2_id != None:
                score[username_id]['remainings'] += 1

        if 'DEC' in method:
            if survivor1:
                score[username_id]['survived'] += 1
            if survivor2:
                score[username_id]['survived'] += 1
            wins, losses = _calc_suv_win_loss(survivor1, survivor2, winner, loser)
            score[username_id]['wins'] += wins
            score[username_id]['losses'] += losses

        if method.startswith('KO') or \
            'TKO' in method or 'SUB' in method:
            if survivor1 and survivor1.get('id') == winner.get('id'):
                score[username_id]['survived'] += 1

            if survivor2 and survivor2.get('id') == winner.get('id'):
                score[username_id]['survived'] += 1
            
            wins, losses = _calc_suv_win_loss(survivor1, survivor2, winner, loser)
            score[username_id]['wins'] += wins
            score[username_id]['losses'] += losses

    entry_views = score.values()
    entry_views = sorted(entry_views, reverse=True,  key=lambda x: (len(x['died'])*-1, x['survived'], x['wins'], x['last_edited']*-1)) 

    for x, entry in enumerate(entry_views):
        entry['ranking'] = x+1
        # not sure whether entry model should be updated at this time regarding ranking
        _entry = get_object_or_404(Entry, pk=entry['id'])
        _entry.ranking = x+1
        _entry.save()

    return entry_views

def get_fight_views(selections):
    bout_views = {}
    for selection in selections:
        # fight/bout view
        _bout = selection.bout
        view_id = f"{_bout.id}"
        view = bout_views.get(view_id, {})
        user = dict(
            username=f'{selection.entry.user.displayname}', 
            status=selection.bout.status
        )
        if not view:
            died = None
            if 'DEC' not in _bout.method:
                died = _bout.loser and _bout.loser.name
            view = dict(
                id=_bout.id,
                fighter1=_bout.fighter1.name,
                fighter2=_bout.fighter2.name,
                winner=_bout.winner and _bout.winner.name,
                loser=_bout.loser and _bout.loser.name,
                died=died,
                draw=_bout.status == 'drawn',
                status=_bout.status,
                method=_bout.method,
                round=_bout.round,
                time=_bout.time,
            )
    
        view['entries_1'] = _count_entries(selection.bout.fighter1.id, selections)
        view['entries_2'] = _count_entries(selection.bout.fighter2.id, selections)

        bout_views[view_id] = view

    _bouts = bout_views.values()
    return sorted(_bouts, key = lambda _bout: _bout['id'])

def get_leaderboard_view(entries):
    data = {}
    for entry in entries:
        _user = entry.user
        view = data.get(_user.id, {})
        if not view:
            view = dict(
                id=_user.id,
                avatar=_user.avatar,
                username=_user.username,
                initials=_user.initials,
                displayname=_user.displayname,
                first_place=0,
                second_place=0,
                third_place=0,
                fq_points=_user.fq_points # fq_points from user
            ) 
            
        if entry.ranking == 1:
            view['first_place'] += 1
            view['fq_points'] += 100 
        elif entry.ranking == 2:
            view['second_place'] += 1
            view['fq_points'] += 10 
        elif entry.ranking == 3:
            view['third_place'] += 1
            view['fq_points'] += 1 

            '''
                FQ points rule
                1st place *100
                2nd place *10
                3rd place *1

            '''

        data[_user.id] = view

    leaderboard_views = data.values()
    # leaderboard_views = sorted(leaderboard_views, reverse=True,  key=lambda x: (x['first_place'], x['second_place'], x['third_place'])) 
    leaderboard_views = sorted(leaderboard_views, reverse=True,  key=lambda x: (x['fq_points']))

    for x, _ in enumerate(leaderboard_views):
        _['ranking'] = x+1

    return leaderboard_views


class EntryViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows entries to be viewed or edited.
    """
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
    permission_classes = [permissions.AllowAny]
    # permission_classes = [permissions.IsAuthenticated]

    @action(methods=['get'], detail=False)
    def check_user_already_taken(self, request, **kwarg):
        entries = self.queryset.filter(user__pk=request.query_params['user_id'])
        status = len(entries) > 0
        return Response(dict(status=status))
 
    @action(methods=['post'], detail=False)
    def get_latestcontest(self, request, **kwarg):
        latest_event = Event.objects.filter(status='upcoming').latest('-date')
        game_id = request.data['game_id']
        if int(game_id) == -1:
            selections = Selection.objects.filter(entry__event_id=latest_event.id, entry__game__isnull=True)
        else:
            selections = Selection.objects.filter(entry__game_id=game_id)

        bout_views = get_fight_views(selections)
        entry_views = get_entry_views(selections)
        games = get_games(latest_event, request.data['game_id'], request.user.id)

        return Response(dict(
            bout_views=bout_views,
            entry_views=entry_views,
            event=EventSerializer(latest_event).data,
            games=games
        ))

    @action(methods=['post'], detail=False)
    def get_contest_history(self, request, **kwarg):
        try:
            user_id = request.user.id
            entries = Entry.objects.filter(user_id=user_id)
            games = []
            for _ in entries:
                game = _.event
                game_id = -1
                if _.game:
                    game_id = _.game.id
                    game = _.game
                ranking = _.ranking
                if _.event.action != 'completed':
                    ranking = '-'
                games.append(dict(
                    id=_.id,
                    event_id=_.event.id,
                    game_id=game_id,
                    status=game.action,
                    name=game.name,
                    date=game.date,
                    ranking=ranking
                ))
                games = sorted(games, reverse=True, key=lambda x: (x['date']))
            return Response(dict(
                games=games,
            ), status=200)
        except Exception as err:
            logger.warning(str(err))
            return Response(dict(
                games=[],
            ), status=400)

    @action(methods=['post'], detail=False)
    def get_contest_history_detail(self, request, **kwarg):
        try:
            event_id = request.data['event_id']
            game_id = request.data['game_id']
            if int(game_id) == -1:
                selections = Selection.objects.filter(entry__event_id=event_id, entry__game__isnull=True)
            else:
                selections = Selection.objects.filter(entry__event_id=event_id, entry__game_id=game_id)

            bout_views = get_fight_views(selections)
            entry_views = get_entry_views(selections)
            event = EventSerializer(Event.objects.get(id=event_id)).data
            return Response(dict(
                bout_views=bout_views,
                entry_views=entry_views,
                event=event,
            ), status=200)
        except Exception as err:
            logger.warning(str(err))
            return Response(dict(
                bout_views=[],
                entry_views=[],
                event={},
            ), status=400)


    @action(methods=['get'], detail=False)
    def get_leaderboard(self, request, **kwarg):
        views = get_leaderboard_view(self.queryset)

        return Response(dict(views=views))

    @action(methods=['post'], detail=False)
    def get_entries(self, request, **kwarg):
        try:
            entries = self.queryset.filter(pk__in=request.data)
            data = []
            for entry in entries:
                data.append(dict(
                    event=entry.event.name,
                    user=entry.user.username
                ))
            return Response(dict(entries=data))
        except Exception as err:
            return Response(dict(entries=[]), status=500)

    def create(self, request):
        try:
            data= request.data['entry']
            entry = None
            entry_serializer = None
            is_exist = False
            message = 'Successfully done.'
            try:
                if data['game'] != -1:
                    entry = Entry.objects.get(event_id=data['event'], user_id=data['user'], game_id=data['game'])
                else:
                    entry = Entry.objects.get(event_id=data['event'], user_id=data['user'], game__isnull=True)
            except:
                pass
            if entry:
                is_exist = True
                message = 'Successfully edited.'
                data['last_edited'] = datetime.now()
                entry_serializer = EntrySerializer(entry, data=data)
            else:
                if data['game'] == -1:
                    data['game'] = None
                entry_serializer = EntrySerializer(data=data)

            if entry_serializer.is_valid():
                entry = entry_serializer.save()

            Selection.objects.filter(entry_id=entry.id).delete()
            for selection in request.data['selections']:
                selection['entry'] = entry.id

            selection_serializer = SelectionSerializer(data=request.data['selections'], many=True)
            if selection_serializer.is_valid():
                selection_serializer.save()
                return Response({'status': 'success', 'message': message})
            
            return Response({'status': 'failed', 'message': 'Something wrong happened.'})
        except Exception as err:
            logger.warning(str(err))
            return Response({'status': 'failed', 'message': 'Something wrong happened.'})

    

  