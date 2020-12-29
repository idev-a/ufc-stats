from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework_extensions.mixins import NestedViewSetMixin
import copy
from allauth.socialaccount.providers.twitter.views import TwitterOAuthAdapter
from rest_auth.registration.views import SocialLoginView
from rest_auth.social_serializers import TwitterLoginSerializer
from requests_oauthlib import OAuth1
from urllib.parse import urlencode
from rest_framework.views import APIView
from django.http import HttpResponse
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
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

    @action(methods=['get'], detail=False)
    def get_latestContest(self, request, **kwarg):
        latest_event = Event.objects.all().filter(status='upcoming').latest('-date')
        entries = Entry.objects.all().filter(event__pk=latest_event.id)
        selections = Selection.objects.all()

        # fight/bout view
        bout_views = {}
        for selection in selections:
            _bout = selection.bout
            view_id = f"{_bout.id}"
            view = bout_views.get(view_id, {})
            user = dict(
                username=f'{selection.entry.user.username}-{selection.entry.id}', 
                fighter=selection.fighter.name,
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
            else:
                if selection.fighter_id == _bout.fighter1_id:
                    view['entries_1'].append(selection.entry.id)
                else:
                    view['entries_2'].append(selection.entry.id)

            bout_views[view_id] = view

        return Response(dict(bouts=bout_views.values(), event=EventSerializer(latest_event).data))

    @action(methods=['get'], detail=False)
    def get_score_by_user(self, request, **kwarg):
        entries = Entry.objects.all().filter(bout__status='completed')
        score = {}
        default_score = {
            'surviving_fighters': 0,
            'wins': 0,
            'losses': 0,
            'dead': 0
        }
        for entry in entries:
            username = entry.user.username
            score[username] = score.get(username, copy.deepcopy(default_score)) 
            method = entry.bout.method
            winner_id = entry.bout.winner.id # winner from bout
            fighter_id = entry.fighter.id # user-selected fighter in the contest
            if method.startswith('S-DEC') or \
                method.startswith('U-DEC') or \
                method.startswith('SUB'):
                if fighter_id == winner_id:
                    score[username]['surviving_fighters'] += 1
                else:
                    score[username]['dead'] += 1
            if method.startswith('KO') or \
                'TKO' in method:
                if fighter_id == winner_id:
                    score[username]['wins'] += 1
                else:
                    score[username]['losses'] += 1

        data = []
        for key, value in score.items():
            value.update({'username': key})
            data.append(value)

        return Response(dict(scores=data))

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
