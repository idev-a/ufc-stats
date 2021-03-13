from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework_extensions.mixins import NestedViewSetMixin

from datetime import datetime as date

from contest.models import (
	Faq,
	Ticket
)
from contest.serializers import (
	FaqSerializer,
	TicketSerializer,
)

from contest.emailagent import send_simple_email

import pdb

class FaqViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
	"""
	API endpoint that allows entries to be viewed or edited.
	"""
	queryset = Faq.objects.all()
	serializer_class = FaqSerializer
	permission_classes = [permissions.AllowAny]
	# permission_classes = [permissions.IsAuthenticated]

	@action(methods=['post'], detail=False)
	def submit_ticket(self, request, **kwarg):
		status = 200
		message = 'Successfully Sent'
		try:
			data = request.data
			username = ''
			if request.user:
				data['creator'] = request.user.id
				username = request.user.username
			data['status'] = send_simple_email(data['title'], data['message'], username, to_email="ideveloper003@gmail.com")
			data['delivered'] = date.now().strftime("%Y-%m-%d %H:%M:%S")
			ticket_serializer = TicketSerializer(data=data)
			if ticket_serializer.is_valid():
				new_ticket = ticket_serializer.save()

		except Exception as err:
			print(err)
			status = 500
			message = 'Something went wrong.'

		return Response(dict(message=message, status=status), status)

