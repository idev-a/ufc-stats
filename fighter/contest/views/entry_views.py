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

def get_entry_views(selections):
    score = {}
    default_score = {
        'id': '',
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
        if bout.status != 'completed':
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
 
    @action(methods=['get'], detail=False)
    def get_latestcontest(self, request, **kwarg):
        latest_event = Event.objects.filter(status='upcoming').latest('-date')
        selections = Selection.objects.filter(entry__event_id=latest_event.id)
        bout_views = get_fight_views(selections)
        entry_views = get_entry_views(selections)

        return Response(dict(bout_views=bout_views, entry_views=entry_views, event=EventSerializer(latest_event).data))

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
        data= request.data['entry']
        entry = None
        entry_serializer = None
        is_exist = False
        message = 'Successfully done.'
        try:
            entry = Entry.objects.get(event_id=data['event'], user_id=data['user'])
        except:
            pass
        if entry:
            is_exist = True
            message = 'Successfully edited.'
            data['last_edited'] = datetime.now()
            entry_serializer = EntrySerializer(entry, data=data)
        else:
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

    

  