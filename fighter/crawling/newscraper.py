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
from contest.util import _valid, convert_date, strip_list1
import pdb

class Scraper:
	upcoming_url = 'http://ufcstats.com/statistics/events/upcoming'
	completed_url = 'http://ufcstats.com/statistics/events/completed'

	def __init__(self):
		self.session = requests.Session()

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

	def start_requests(self):
		while True:
			print('[scraper] started')

			# upcoming events
			# res = self.session.get(self.upcoming_url)
			# self.parse_event(Selector(text=res.content))

			# scan db to get the scraped events to get the stats
			events = Event.objects.all().filter(status='upcoming')
			if events:
				event = events.latest('-date')
				res = self.session.get(event.detail_link)
				meta = {'event_id': event.id}

				self.parse_bout_list(Selector(text=res.content), meta)

			time.sleep(60)

	def parse_event(self, response):
		print('[scraper] Parse Event ---')
		trs = response.css('table.b-statistics__table-events tr.b-statistics__table-row')
		if len(trs) > 2:
			for tr in trs[2:]:
				name = _valid(tr.css('a::text').get())
				detail_link = _valid(tr.css('a').xpath('@href').get())
				location = _valid(tr.xpath('.//td[2]/text()').get())
				date = _valid(tr.css('span.b-statistics__date::text').get())
				item = dict(
					name=name,
					date=convert_date(date),
					location=location,
					detail_link=detail_link,
					status='upcoming'
				)

				event_id = self.save_event(item)

				res = self.session.get(detail_link)
				meta = {'event_id': event_id}
				self.parse_bout_list(Selector(text=res.content), meta)

	def parse_bout_list(self, response, meta):
		print('[scraper] parse_bout_list ---', meta)
		event_id = meta['event_id']
		event = Event.objects.get(pk=event_id)
		trs = response.css('table.b-fight-details__table tr.b-fight-details__table-row')
		if trs:
			new_bouts = []
			cnt_completed = 0
			for tr in trs[1:]:
				fight_detail = strip_list1(tr.xpath('.//td[1]//text()').getall())
				detail_link = tr.xpath('@data-link').get()
				fighters = strip_list1(tr.xpath('.//td[2]/p/a/text()').getall())
				weight_class = _valid(tr.xpath('.//td[7]/p/text()').get())
				method = _valid(' '.join(strip_list1(tr.xpath('.//td[8]//text()').getall())))
				go_the_distance = True if 'dec' in _valid(method) else False
				round = _valid(tr.xpath('.//td[9]/p/text()').get()) or 0
				round_time = _valid(tr.xpath('.//td[10]/p/text()').get())

				item = dict(
					fighter1=self.save_fighter({'name': fighters[0]}).id,
					fighter2=self.save_fighter({'name': fighters[1]}).id,
					weight_class=weight_class,
					method=method,
					round=round,
					time=round_time,
					go_the_distance=go_the_distance,
					detail_link=detail_link,
					status='pending',
					event=event.id
				)
				bout = self.save_bout(item)
				new_bouts.append(bout.id)

				if fight_detail:
					cnt_completed += 1
					if cnt_completed != len(trs[1:]) and event.action != 'started':
						notify_data = {
							'event': {
								'action': 'started',
							},
							'message': 'Event already started.'
						}
						event.action = 'started'
					elif cnt_completed == len(trs[1:]):
						notify_data = {
							'event': {
								'action': 'completed',
							},
							'message': 'All fights were completed.'
						}
						event.action == 'completed'
					else:
						notify_data = {
							'bout': True,
							'refresh': True,
							'message': f'The fight between {bout.fighter1.name} vs. {bout.fighter2.name} was completed.'
						}
					event.save()
					self.notify_user(notify_data)
				try:
					res = self.session.get(detail_link)
					meta = {'bout_id': bout.id}
					self.parse_bout_detail(Selector(text=res.content), meta)
				except:
					pass

			# Compare new bouts with old ones to check if there is any bouts cancelled
			# delete cancelled bouts due to fighters before d-day
			self.delete_cancelled_bouts(event_id, new_bouts)

			time.sleep(1)

	def parse_bout_detail(self, response, meta):
		print('[scraper] parse_bout_detail ---', meta)
		bout_id = meta['bout_id']
		bout = Bout.objects.get(pk=bout_id)

		persons = response.css('div.b-fight-details__person')
		for person in persons:
			not_yet_finished = person.css('i.b-fight-details__person-status_style_none')
			if not not_yet_finished:
				bout.status='completed'
				bout.save()

			marks = _valid(person.css('i::text').get())
			name = _valid(person.css('div.b-fight-details__person-text h3 a::text').get())
			title = _valid(person.css('div.b-fight-details__person-text p.b-fight-details__person-title::text').get())
			if marks: # bout finished
				fighter = self.get_fighter(name)
				if marks == 'W':
					bout.winner = fighter
				elif marks == 'L':
					bout.loser = fighter
				elif marks == 'D':
					bout.status='drawn'
					
				bout.save()

			self.update_fighter_in_bout(bout, name, title.replace('"', ''))

			time.sleep(1)

	def get_fighter(self, name):
		return Fighter.objects.get(name=name)

	def update_fighter_in_bout(self, bout, name, title):
		fighter = None
		try:
			if bout.fighter1.name == name:
				fighter = bout.fighter1
			elif bout.fighter2.name == name:
				fighter = bout.fighter2

			fighter.title = title
			fighter.save()
		except:
			pass

	def delete_cancelled_bouts(self, event_id, new_bouts):
		queryset = Bout.objects.all().filter(event_id=event_id).exclude(pk__in=new_bouts)
		if queryset:
			print('[scraper] delete cancelled bouts', queryset)
			queryset.delete()

			message = f'{queryset.count()} bout was cancelled.'
			if queryset.count() > 1:
				message = f'{queryset.count()} bouts were cancelled.'

			notify_data = {
				'refresh': True,
				'message': message

			}
			self.notify_user(notify_data)

	def save_bout(self, item):
		bout = None
		bout_serializer = None
		try:
			bout = Bout.objects.get(detail_link=item['detail_link'])
		except:
			pass

		if bout:
			bout_serializer = BoutSerializer(bout, data=item)
		else:
			bout_serializer = BoutSerializer(data=item)
		if bout_serializer.is_valid():
			bout = bout_serializer.save()
		else:
			print('[save_bout] error', bout_serializer.errors)

		return bout

	def save_fighter(self, item):
		print('[scraper] save_fighter ---', item)
		fighter = None
		try:
			fighter = Fighter.objects.get(name=item['name'])
		except:
			pass
		if not fighter:
			fighter_serializer = FighterSerializer(data=item)
			if fighter_serializer.is_valid():
				fighter = fighter_serializer.save()

		return fighter

	def save_event(self, item):
		print('[scraper] save_event ---', item)
		event = None
		try:
			event = Event.objects.get(name=item['name'], date=item['date'])
		except:
			pass
		if not event:
			event_serializer = EventSerializer(data=item)
			event_serializer.is_valid()
			event_serializer.save()
			return event_serializer.data['id']
		else:
			return event.id


if __name__ == '__main__':
	scraper = Scraper()
	scraper.start_requests()

