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
from datetime import datetime, timedelta
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

def _update_game_rank(selections):
    entry_views = get_entry_views(selections)
    status = 200
    try:
        total_quaked = 0
        for _ in entry_views:
            if _['died']:
                total_quaked += 1

        for _ in entry_views:
            entry = get_object_or_404(Entry, pk=_['id'])
            if entry.game and entry.game.genre != 'free':
                if total_quaked == len(entry_views):
                    # should refund buyin
                    entry.user.coins += entry.game.buyin
                if _['ranking'] == 1 and len(_['died']) == 0:
                    entry.user.coins += entry.game.prize

                entry.user.save()
    except Entry.DoesNotExist:
        status = 404
    return status

def update_rank(event_id):
    # Single Game
    selections = Selection.objects.filter(entry__event_id=event_id, entry__game__isnull=True)
    status = _update_game_rank(selections)

    # Mutiple games
    games = Game.objects.filter(event_id=event_id)
    for game in games:
        selections = Selection.objects.filter(entry__event_id=event_id, entry__game_id=game.id)
        status = _update_game_rank(selections)

    return Response(dict(message='ok', status=status))

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
        entry_name = selection.entry.user.displayname
        if selection.entry.retry_number:
            entry_name += f' ({selection.entry.retry_number})'
        score[username_id]['entry'] = entry_name
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
        if bout.status == 'started' or bout.status == 'pending':
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

        # some bouts end with no contest, UFC says CNC
        # we consider those fighters survive, and neither wins
        if bout.method == 'CNC':
            if survivor1:
                score[username_id]['survived'] += 1
            if survivor2:
                score[username_id]['survived'] += 1

    entry_views = score.values()
    entry_views = sorted(entry_views, reverse=True,  key=lambda x: (len(x['died'])*-1, x['survived'], x['wins'], x['last_edited']*-1)) 

    ranking = 1
    prev_entry = {}
    for x, entry in enumerate(entry_views):
        if x > 0:
            prev_entry = entry_views[x-1]
        if prev_entry:
            if prev_entry['survived'] != entry['survived'] or prev_entry['wins'] != entry['wins']:
                ranking += 1
        entry['ranking'] = ranking
        # not sure whether entry model should be updated at this time regarding ranking
        _entry = get_object_or_404(Entry, pk=entry['id'])
        _entry.survived = entry['survived']
        _entry.wins = entry['wins']
        _entry.quaked = len(entry['died'])
        _entry.ranking = ranking
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
                coins=_user.coins # coins from user
            ) 
            
        if entry.ranking == 1:
            view['first_place'] += 1
            # view['coins'] += 100 
        elif entry.ranking == 2:
            view['second_place'] += 1
            # view['coins'] += 10 
        elif entry.ranking == 3:
            view['third_place'] += 1
            # view['coins'] += 1 

            '''
                FQ points rule
                1st place *100
                2nd place *10
                3rd place *1

            '''

        data[_user.id] = view

    leaderboard_views = data.values()
    # leaderboard_views = sorted(leaderboard_views, reverse=True,  key=lambda x: (x['first_place'], x['second_place'], x['third_place'])) 
    leaderboard_views = sorted(leaderboard_views, reverse=True,  key=lambda x: (x['coins']))

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
        games = Game.objects.get_games(latest_event, request.user.id)

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
                    status=_.event.action,
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
            event_id = int(request.data['event_id'])
            game_id = int(request.data['game_id'])
            game = None
            if game_id == -1:
                selections = Selection.objects.filter(entry__event_id=event_id, entry__game__isnull=True)
                _event = Event.objects.get(id=event_id)
                game = dict(
                    id=-1,
                    name=_event.name,
                    event=EventSerializer(_event).data,
                    type_of_registration='public',
                    date=_event.date,
                    action=_event.action,
                    genre='free',
                    buyin=0,
                    prize=0
                )
            else:
                _ = Game.objects.get(id=game_id)
                game = dict(
                    id=_.id,
                    name=_.name,
                    event=EventSerializer(_.event).data,
                    type_of_registration=_.type_of_registration,
                    joined_users=UserSerializer(_.joined_users.all(), many=True).data,
                    entrants=UserSerializer(_.entrants.all(), many=True).data,
                    instructions=_.instructions,
                    rules_set=_.rules_set,
                    date=_.date,
                    action=_.action,
                    genre=_.genre,
                    buyin=_.buyin,
                    prize=_.prize,
                )
                selections = Selection.objects.filter(entry__event_id=event_id, entry__game_id=game_id)

            bout_views = get_fight_views(selections)
            entry_views = get_entry_views(selections)
            return Response(dict(
                bout_views=bout_views,
                entry_views=entry_views,
                game=game,
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

    def bout_not_cancelled(self, _data, fighter):
        is_exist = False
        for bout in _data.get('bouts', []):
            if fighter.id in [bout['fighter1'], bout['fighter2']]:
                is_exist = True
                bout.get('survivors', []).append(fighter.id)
                bout['contests'].append(fighter.id)
                bout['contests_orig'].append(fighter.id)
                break
        return is_exist

    def add_fighters(self, event, data):
        bouts = Bout.objects.filter(event__id=event.id)
        bouts_dict = BoutSerializer(bouts, many=True).data
        for bout in bouts_dict:
            bout['contests'] = []
            bout['contests_orig'] = []

        for bout in bouts:
            fighter = FighterSerializer(bout.fighter1).data
            if fighter not in data['fighters']:
                data['fighters'].append(fighter)
            fighter = FighterSerializer(bout.fighter2).data
            if fighter not in data['fighters']:
                data['fighters'].append(fighter)
        return bouts_dict

    def is_new_team_data(self, _data, cur_data):
        is_new = True
        for _ in _data['teams']:
             if _['key'] == cur_data['key']:
                cur_data = _
                is_new = False
                break
        return is_new, cur_data

    @action(methods=['post'], detail=False)
    def get_my_teams(self, request, **kwarg):
        ''' 
            data for My Teams page
            requirs user info
        '''
        status = 200
        live_data = {'fighters': [], 'teams': []}
        recent_data = {'fighters': [], 'teams': []}
        option = request.data.get('option', 30)
        min_dt = datetime.now() - timedelta(days=option)
        date_range = (min_dt, datetime.now())
        selections = Selection.objects.filter(entry__user_id=request.user.id).filter(entry__last_edited__range=date_range)
        try:
            if request.user:
                latest_event = Event.objects.filter(status='upcoming').latest('-date')
                live_bouts_dict = self.add_fighters(latest_event, live_data)

                for sel in selections:
                    event = sel.entry.event
                    game = sel.entry.game
                    retry_number = sel.entry.retry_number
                    key = game.id if game else f'e_{event.id}'
                    if retry_number:
                        key = f"{key}_{retry_number}"
                    # main contest, live contest
                    cur_data = {'key':key, 'game': {}, 'fighters': []}
                    is_new = True
                    if event.id == latest_event.id:
                        is_new, cur_data = self.is_new_team_data(live_data, cur_data)
                        if is_new:
                            cur_data['bouts'] = copy.deepcopy(live_bouts_dict)
                            live_data['teams'].append(cur_data)
                    else:
                        # recent games
                        recent_bouts_dict = self.add_fighters(event, recent_data)
                        is_new, cur_data = self.is_new_team_data(recent_data, cur_data)
                        if is_new:
                            cur_data['bouts'] = copy.deepcopy(recent_bouts_dict)
                            recent_data['teams'].append(cur_data)

                    if is_new:
                        cur_data.get('game',{})['event'] = EventSerializer(event).data
                        cur_data.get('game',{})['id'] = game.id if game else -1
                        cur_data.get('game',{})['name'] = game.name if game else event.name
                        cur_data.get('game',{})['buyin'] = game.buyin if game else 0
                        cur_data.get('game',{})['prize'] = game.prize if game else 0
                        cur_data.get('game',{})['genre'] = game.genre if game else 'free'
                        cur_data.get('game',{})['retry_number'] = retry_number
                    if sel.survivor1 and self.bout_not_cancelled(cur_data, sel.survivor1):
                        cur_data.get('fighters',[]).append(sel.survivor1.id)
                    if sel.survivor2 and self.bout_not_cancelled(cur_data, sel.survivor2):
                        cur_data.get('fighters',[]).append(sel.survivor2.id)
            else:
                return Response(dict(live_data={}, recent_data={}), status=400)
        except Exception as err:
            logger.warning(str(err))
            status = 500

        live_data['teams'] = sorted(live_data['teams'], key=lambda x: (x['game']['id'], x['game']['retry_number']))
        recent_data['teams'] = sorted(recent_data['teams'], reverse=True, key=lambda x: (x['game']['id'], x['game']['retry_number'], x['game']['event']['date']))
        return Response(dict(live_data=live_data, recent_data=recent_data), status=status)

    @action(methods=['get'], detail=False)
    def test_update_rank(self, request, **kwarg):
        event_id = request.query_params['event_id']
        if event_id:
            update_rank(event_id)
        return Response(dict(message='ok'))

    def create(self, request):
        try:
            data= request.data['entry']
            entry = None
            entry_serializer = None
            is_exist = False
            message = 'Successfully done.'
            try:
                if int(data['game']) != -1:
                    entry = Entry.objects.get(event_id=data['event'], user_id=data['user'], game_id=data['game'], retry_number=data['retry_number'])
                else:
                    entry = Entry.objects.get(event_id=data['event'], user_id=data['user'], game__isnull=True)
            except:
                pass
            if entry:
                if entry.game and data['retry_number'] > entry.game.retry_times:
                    raise Exception
                is_exist = True
                message = 'Successfully edited.'
                data['last_edited'] = datetime.now()
                entry_serializer = EntrySerializer(entry, data=data)
            else:
                if data['game'] == -1:
                    data['game'] = None
                entry_serializer = EntrySerializer(data=data)

            # update entry information
            if entry_serializer.is_valid():
                entry = entry_serializer.save()

            # delete old selections and save new data
            Selection.objects.filter(entry_id=entry.id).delete()
            for selection in request.data['selections']:
                selection['entry'] = entry.id

            selection_serializer = SelectionSerializer(data=request.data['selections'], many=True)
            if selection_serializer.is_valid():
                selection_serializer.save()
                return Response({'status': 'success', 'message': message})
            
            return Response({'status': 'failed', 'message': 'Something wrong happened.'}, status=400)
        except Exception as err:
            logger.warning(str(err))
            print(str(err))
            return Response({'status': 'failed', 'message': 'Something wrong happened.'}, status=400)

    

  