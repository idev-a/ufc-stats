from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework_extensions.mixins import NestedViewSetMixin

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from django.conf import settings

from contest.models import (
    Faq
)
from contest.serializers import (
    FaqSerializer,
)

import pdb

class FaqViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows entries to be viewed or edited.
    """
    queryset = Faq.objects.all()
    serializer_class = FaqSerializer
    permission_classes = [permissions.AllowAny]
    # permission_classes = [permissions.IsAuthenticated]
