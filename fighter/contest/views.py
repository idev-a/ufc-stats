from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework_extensions.mixins import NestedViewSetMixin

from django.contrib.auth.models import User, Group
from contest.models import (
    Event,
    Bout,
    Fighter,
    Entry
)
from contest.serializers import (
	UserSerializer,
	GroupSerializer,
	EventSerializer,
	BoutSerializer,
	FighterSerializer,
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
        latest_event = Event.objects.all().filter(status='upcoming').latest('-date')
        bouts = Bout.objects.filter(event__pk=latest_event.id)
        return Response(dict(
            bouts=BoutSerializer(bouts, many=True).data,
            event=EventSerializer(latest_event).data
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
        bouts = entries.values_list('bout_id').distinct()
        dead_users = [entry.user_id for entry in entries.filter(finished=True, status=False)]
        contests = []
        for bout in bouts:
            _bout = Bout.objects.get(pk=bout[0])
            users = []
            for ii in entries.filter(bout_id=bout[0]):
                status = True
                if ii.user_id in dead_users:
                    status = False
                users.append(dict(
                   username=f'{ii.user.username}-{ii.id}', 
                   fighter=ii.fighter.name,
                   status=status,
                   finished=ii.finished
                ))
            contests.append({
                'fighter1': _bout.fighter1.name,
                'fighter2': _bout.fighter2.name,
                'winner': _bout.winner and _bout.winner.name,
                'loser': _bout.loser and _bout.loser.name,
                'users': users,
                'status': _bout.status
            })

        return Response(dict(contests=contests, event=EventSerializer(latest_event).data))

    def create(self, request):
        serializer = EntrySerializer(many=True, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'success', 'message': 'Successfully done.'})

        return Response({'status': 'failed', 'message': 'Something wrong happened.'})

