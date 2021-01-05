from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework_extensions.mixins import NestedViewSetMixin
import copy
from requests_oauthlib import OAuth1
from urllib.parse import urlencode
from rest_framework.views import APIView
from django.conf import settings
import requests

from django.contrib.auth.models import User, Group
from contest.models import (
    Event,
    Bout,
    Fighter,
    Selection,
    Entry
)
from contest.serializers import (
	UserSerializer,
	GroupSerializer,
	EventSerializer,
	BoutSerializer,
	FighterSerializer,
    SelectionSerializer,
    EntrySerializer
)

from allauth.socialaccount.providers.twitter.views import TwitterOAuthAdapter
from rest_auth.registration.views import SocialLoginView
from rest_auth.social_serializers import TwitterLoginSerializer

import pdb

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

class EventViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows events to be viewed or edited.
    """
    queryset = Event.objects.all().order_by('date')
    serializer_class = EventSerializer
    permission_classes = [permissions.AllowAny]
    # permission_classes = [permissions.IsAuthenticated]

    @action(methods=['get'], detail=False)
    def get_latestevent(self, request, **kwarg):
        events = Event.objects.all().filter(status='upcoming')
        if events:
            latest_event = events.latest('-date')
            bouts = Bout.objects.filter(event__id=latest_event.id)
            return Response(dict(
                bouts=BoutSerializer(bouts, many=True).data,
                event=EventSerializer(latest_event).data
            ))
        else:
            return Response(dict(
                bouts=[],
                event=None
            ))

class BoutViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows bouts to be viewed or edited.
    """
    queryset = Bout.objects.all()
    serializer_class = BoutSerializer
    # permission_classes = [permissions.IsAuthenticated]

class FighterViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows fighters to be viewed or edited.
    """
    queryset = Fighter.objects.all()
    serializer_class = FighterSerializer
    permission_classes = [permissions.AllowAny]
    # permission_classes = [permissions.IsAuthenticated]

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
        entries = Entry.objects.all().filter(user__pk=request.query_params['user_id'])
        status = len(entries) > 0
        return Response(dict(status=status))

    def get_fight_views(self, selections):
        bout_views = {}
        for selection in selections:
            # fight/bout view
            _bout = selection.bout
            view_id = f"{_bout.id}"
            view = bout_views.get(view_id, {})
            user = dict(
                username=f'{selection.entry.user.username}-{selection.entry.id}', 
                status=selection.bout.status
            )
            if not view:
                view = dict(
                    id=_bout.id,
                    fighter1=_bout.fighter1.name,
                    fighter2=_bout.fighter2.name,
                    winner=_bout.winner and _bout.winner.name,
                    loser=_bout.loser and _bout.loser.name,
                    status=_bout.status,
                    method=_bout.method,
                    round=_bout.round,
                    time=_bout.time,
                    entries_1=[],
                    entries_2=[],
                )
        
            if selection.survivor1_id:
                view['entries_1'].append(selection.entry.id)
            if selection.survivor2_id:
                view['entries_2'].append(selection.entry.id)

            bout_views[view_id] = view

        return bout_views.values()

    def get_entry_views(self, selections):
        score = {}
        default_score = {
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
            username_id = f'{selection.entry.user.username}-{selection.entry.id}'
            bout = selection.bout
            method = bout.method

            winner_id = bout.winner and bout.winner.id # winner from bout
            score[username_id] = score.get(username_id, copy.deepcopy(default_score))
            score[username_id]['entry'] = username_id
            fighter1 = bout.fighter1.name
            fighter2 = bout.fighter2.name
            winner = bout.winner and bout.winner.name
            loser = bout.loser and bout.loser.name
            score[username_id]['method'] = method
            if fighter1 not in score[username_id]['fighters']:
                score[username_id]['fighters'].append(fighter1)

            if fighter2 not in score[username_id]['fighters']:
                score[username_id]['fighters'].append(fighter2)

            if winner and winner not in score[username_id]['winners']:
                score[username_id]['winners'].append(winner)

            if loser and loser not in score[username_id]['losers']:
                score[username_id]['losers'].append(loser)

                if 'DEC' not in bout.method and loser not in score[username_id]['died']:
                    score[username_id]['died'].append(loser)


            # remainings
            if bout.status != 'completed':
                score[username_id]['remainings'] += 1

            if 'DEC' in method:
                score[username_id]['survived'] += 2
                score[username_id]['wins'] += 1
                score[username_id]['losses'] += 1

            if method.startswith('KO') or \
                'TKO' in method or 'SUB' in method:

                score[username_id]['survived'] += 1
                score[username_id]['wins'] += 1
                score[username_id]['losses'] += 1

        return score.values()

    @action(methods=['get'], detail=False)
    def get_latestContest(self, request, **kwarg):
        latest_event = Event.objects.all().filter(status='upcoming').latest('-date')
        selections = Selection.objects.all()

        bout_views = self.get_fight_views(selections)
        entry_views = self.get_entry_views(selections)

        return Response(dict(bout_views=bout_views, entry_views=entry_views, event=EventSerializer(latest_event).data))

    @action(methods=['post'], detail=False)
    def get_entries(self, request, **kwarg):
        try:
            entries = Entry.objects.all().filter(pk__in=request.data)
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
        entry_serializer = EntrySerializer(data=request.data['entry'])
        if entry_serializer.is_valid():
            entry = entry_serializer.save()
            for selection in request.data['selections']:
                selection['entry'] = entry.id

            selection_serializer = SelectionSerializer(data=request.data['selections'], many=True)
            if selection_serializer.is_valid():
                selection_serializer.save()
                return Response({'status': 'success', 'message': 'Successfully done.'})

        return Response({'status': 'failed', 'message': 'Something wrong happened.'})


# Social
class TwitterLogin(SocialLoginView):
    serializer_class = TwitterLoginSerializer
    adapter_class = TwitterOAuthAdapter


class TwitterAuthRedirectEndpoint(APIView):
    def get(self, request, *args, **kwargs):
        try:
            oauth = OAuth1(
                settings.TWITTER_API_KEY, 
                client_secret=settings.TWITTER_API_SECRET_KEY
            )
             #Step one: obtaining request token
            request_token_url = "https://api.twitter.com/oauth/request_token"
            data = urlencode({
                "oauth_callback": settings.TWITTER_AUTH_CALLBACK_URL
            })
            response = requests.post(request_token_url, auth=oauth, data=data)
            response.raise_for_status()
            response_split = response.text.split("&")
            oauth_token = response_split[0].split("=")[1]
            oauth_token_secret = response_split[1].split("=")[1]  

            #Step two: redirecting user to Twitter
            twitter_redirect_url = (f"https://api.twitter.com/oauth/authenticate?oauth_token={oauth_token}")
            return Response(dict(twitter_redirect_url=twitter_redirect_url), status=200)
        except ConnectionError:
            return Response(dict(message=["You have no internet connection"]), status=403)
        except Exception as err:
            print(err)
            return Response(dict(message=["Something went wrong.Try again."]), status=403)


class TwitterCallbackEndpoint(APIView):
    def get(self, request, *args, **kwargs):
        try:
            oauth_token = request.query_params.get("oauth_token")
            oauth_verifier = request.query_params.get("oauth_verifier")
            oauth = OAuth1(
                settings.TWITTER_API_KEY,
                client_secret=settings.TWITTER_API_SECRET_KEY,
                resource_owner_key=oauth_token,
                verifier=oauth_verifier,
            )
            res = requests.post(
                f"https://api.twitter.com/oauth/access_token", auth=oauth
            )
            res_split = res.text.split("&")
            oauth_token = res_split[0].split("=")[1]
            oauth_secret = res_split[1].split("=")[1]

            print(res.text)

            formdata = {
                'access_token': oauth_token,
                'token_secret': oauth_secret
            }
            url = f"{request.scheme}://{request.get_host()}/auth/twitter/"
            res = requests.post(url, data=formdata).json()
            return Response(dict(key=res['key']))
        except ConnectionError:
            return Response(dict(message=["You have no internet connection"]), status=403)
        except Exception as err:
            print(err)
            return Response(dict(message=["Something went wrong.Try again."]), status=403)
