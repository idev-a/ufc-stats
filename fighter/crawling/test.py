import os
import sys
import django

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "."))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fighter.settings')
django.setup()

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
from django.conf import settings
from scrapy.selector import Selector
import requests
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import time

from contest.models import (
	Event,
	Fighter,
	Bout,
	Entry
)
from contest.serializers import (
	EventSerializer,
	BoutSerializer,
	FighterSerializer
)
from contest.utils import _valid, convert_date, strip_list1
import pdb

class Test:

	def __init__(self):
		pass

	def notify_user(self, data): 
		print('[scraper] notify_user', data)
		'''
			{
				'event': {
					'started': True
				},
				'refresh': {
					'cancelled': True
				},
				'refresh': True
			},
		'''
		channel_layer = get_channel_layer()
		async_to_sync(channel_layer.group_send)(
			'UFC',
			{
				'type': 'live_score',
				'data': data
			}
		)

	def run(self):
		self._scan_events()

		self._scan_bouts()

	def _scan_bouts(self):
		events = Event.objects.all().filter(status='upcoming')
		if events:
			event = events.latest('-date')
			bouts = Bout.objects.all().filter(event_id=event.id)
			for bout in bouts:
				if bout.status == 'completed':
					notify_data = {
						'bout': True,
						'refresh': True,
						'message': f'The fight between {bout.fighter1.name} vs. {bout.fighter2.name} was completed.'
					}
					self.notify_user(notify_data)

					time.sleep(5)

	def _scan_events(self):
		# scan db to get the scraped events to get the stats
		events = Event.objects.all().filter(status='upcoming')
		if events:
			event = events.latest('-date')
			if event.action != 'started': 
				notify_data = {
					'event': {
						'action': 'started',
					},
					'message': 'Event already started.',
					'refresh': True
				}
				self.notify_user(notify_data)


if __name__ == '__main__':
	test = Test()
	while True:
		notify_data = {
			'bout': True,
			'refresh': True,
			'message': 'test'
		}
		test.notify_user(notify_data)

		time.sleep(3)