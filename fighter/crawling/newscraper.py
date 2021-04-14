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
from lxml import html
from bs4 import BeautifulSoup as bs
from datetime import datetime
import argparse
import re

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
from contest.views.entry_views import update_rank
from contest.commons import create_main_contest
from contest.utils import _valid, convert_date, strip_list1

import pdb
from contest.logger import logger
# import logging as logger
# logger.basicConfig(
# 	filename='contest.log',
# 	level=logger.INFO,
# 	format="%(asctime)s:%(levelname)s:%(message)s [in %(pathname)s:%(lineno)d]"
# )  

_headers = {
	"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
	"accept-encoding": "gzip, deflate, br",
	"accept-language": "en-US,en;q=0.9,ko;q=0.8",
	"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36"
}

class Scraper:
	upcoming_url = 'http://ufcstats.com/statistics/events/upcoming'
	completed_url = 'http://ufcstats.com/statistics/events/completed'
	espn_url = 'https://www.espn.com/mma/fightcenter'

	def __init__(self):
		self.session = requests.Session()

	def notify_user(self, data): 
		logger.info(f'[scraper] notify_user {json.dumps(data)}')
		'''
			{
				'event': {
					'started': True
				},
				'refresh': True,
			},
		'''
		channel_layer = get_channel_layer()
		async_to_sync(channel_layer.group_send)(
			'UFC_chat',
			{
				'type': 'live_score',
				'data': data
			}
		)

	def start_events(self):
		# upcoming events
		res = self.session.get(self.upcoming_url)
		self.parse_event(Selector(text=res.content))

	def start_bouts(self):
		while True:
			logger.info('[scraper] started ***************')
			# scan db to get the scraped events to get the stats
			events = Event.objects.filter(status='upcoming')
			if events:
				event = events.latest('-date')
				res = self.session.get(event.detail_link)
				meta = {'event_id': event.id}
				# espn_name, espn_date, espn_time = self.info_from_espn()
				# event_date = event.date.strftime('%B %d, %Y')
				# print(f'espn_time, espn_date ', espn_time, espn_date)
				# if event_date == espn_date and event.name == espn_name and espn_time != 'LIVE':
				# 	event.date = convert_date(f"{event_date} {espn_time}")
				# 	event.save()
				self.parse_bout_list(Selector(text=res.content), meta)

			time.sleep(10)

	def info_from_espn(self):
		name = date = _time = ''
		try:
			soup = bs(self.session.get(self.espn_url, headers=_headers).text, 'lxml')
			name = soup.select_one('h1.headline').text
			date = soup.select_one('div.n6.mb2').text
			card = soup.select('span.MMAHeaderUpsellTunein__Meta')[-1].text
			_time = card
			if card != 'LIVE':
				_time = datetime.strptime(card, '%I:%M %p').strftime('%H:%M:%S')
		except Exception as err:
			logger.warning(str(err))
			
		return name, date, _time

	def parse_event(self, response):
		logger.info('[scraper] Parse Event ---')
		trs = response.css('table.b-statistics__table-events tr.b-statistics__table-row')
		default_time = ' 18:00:00'
		espn_name, espn_date, espn_time = self.info_from_espn()
		if len(trs) > 2:
			for tr in trs[2:]:
				name = _valid(tr.css('a::text').get())
				detail_link = _valid(tr.css('a').xpath('@href').get())
				location = _valid(tr.xpath('.//td[2]/text()').get())
				date = _valid(tr.css('span.b-statistics__date::text').get())
				if name == espn_name and date == espn_date and espn_time != 'LIVE':
					date += ' ' + espn_time
				else:
					date += default_time

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
		logger.info(f'[scraper] parse_bout_list --- {json.dumps(meta)}')
		event_id = meta['event_id']
		event = Event.objects.get(pk=event_id)
		event.name = response.css('span.b-content__title-highlight::text').get()
		event.save()
		trs = response.css('table.b-fight-details__table tr.b-fight-details__table-row')
		if trs:
			new_bouts = []
			cnt_completed = 0
			for x, tr in enumerate(trs[1:]):
				fight_detail = strip_list1(tr.xpath('.//td[1]//text()').getall())
				detail_link = tr.xpath('@data-link').get()
				fighters = strip_list1(tr.xpath('.//td[2]/p/a/text()').getall())
				weight_class = _valid(tr.xpath('.//td[7]/p/text()').get())
				method = _valid(' '.join(strip_list1(tr.xpath('.//td[8]//text()').getall())))
				go_the_distance = True if 'dec' in _valid(method) else False
				round = _valid(tr.xpath('.//td[9]/p/text()').get()) or 0
				round_time = _valid(tr.xpath('.//td[10]/p/text()').get())

				gender = 'M'
				if re.search(r'women', weight_class, re.IGNORECASE):
					gender = 'F'
				item = dict(
					fighter1=self.save_fighter({'name': fighters[0], 'gender': gender}).id,
					fighter2=self.save_fighter({'name': fighters[1], 'gender': gender}).id,
					weight_class=weight_class,
					method=method,
					round=round,
					time=round_time,
					go_the_distance=go_the_distance,
					detail_link=detail_link,
					status='pending',
					event=event_id,
					order=x+1
				)
				bout, is_notified = self.save_bout(item)
				new_bouts.append(bout.id)

				print('========================= action', event.action)

				if fight_detail:
					bout.status = 'completed'
					bout.save()

					notify_data = None
					cnt_completed += 1
					if cnt_completed != len(trs[1:]) and not event.action:
						notify_data = {
							'type': 'live_score',
							'refresh': True,
							'event': {
								'action': 'started',
							},
							'message': 'Event just started.'
						}
						event.action = 'started'
					elif cnt_completed == len(trs[1:]) and event.action != 'completed':
						notify_data = {
							'type': 'live_score',
							'refresh': True,
							'event': {
								'action': 'completed',
							},
							'message': 'All fights were completed.'
						}
						event.action = 'completed'
						update_rank(event.id)
						# create_main_contest(event)
					elif not is_notified:
						notify_data = {
							'type': 'live_score',
							'bout': True,
							'refresh': True,
							'message': f'The fight between {bout.fighter1.name} vs. {bout.fighter2.name} was completed.'
						}
					event.save()
					if notify_data:
						self.notify_user(notify_data)
				try:
					res = self.session.get(detail_link)
					meta = {'bout_id': bout.id}
					self.parse_bout_detail(Selector(text=res.content), meta)
				except:
					pass

				time.sleep(1)

			# Compare new bouts with old ones to check if there is any bouts cancelled
			# delete cancelled bouts due to fighters before d-day
			self.delete_cancelled_bouts(event_id, new_bouts)


	def parse_bout_detail(self, response, meta):
		logger.info(f'[scraper] parse_bout_detail --- {json.dumps(meta)}')
		bout_id = meta['bout_id']
		bout = Bout.objects.get(pk=bout_id)

		persons = response.css('div.b-fight-details__person')
		for person in persons:
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
		queryset = Bout.objects.filter(event_id=event_id).exclude(pk__in=new_bouts)
		if queryset:
			logger.info(f'[scraper] delete cancelled bouts {queryset.count()}')

			message = f'{queryset.count()} bout was cancelled.'
			if queryset.count() > 1:
				message = f'{queryset.count()} bouts were cancelled.'

			queryset.delete()
			notify_data = {
				'refresh': True,
				'message': message

			}
			self.notify_user(notify_data)
			time.sleep(3)

	def save_bout(self, item):
		bout = None
		bout_serializer = None
		is_notified = False
		try:
			bout = Bout.objects.get(detail_link=item['detail_link'])
			is_notified = bout.status != 'pending'
		except:
			pass

		if bout:
			bout_serializer = BoutSerializer(bout, data=item)
		else:
			bout_serializer = BoutSerializer(data=item)
		if bout_serializer.is_valid():
			bout = bout_serializer.save()
		else:
			logger.warning(f'[save_bout] error') 

		return bout, is_notified

	def save_fighter(self, item):
		logger.info(f'[scraper] save_fighter --- {json.dumps(item)}')
		fighter = None
		try:
			fighter = Fighter.objects.get(name=item['name'])
		except:
			pass
		if not fighter:
			fighter_serializer = FighterSerializer(data=item)
			if fighter_serializer.is_valid():
				fighter = fighter_serializer.save()
		else:
			fighter.gender = item['gender']
			fighter.title = item.get('title', '')
			fighter.save()

		return fighter

	def save_event(self, item):
		logger.info(f'[scraper] save_event --- {json.dumps(item)}')
		event = None
		try:
			event = Event.objects.get(detail_link=item['detail_link'].strip())
		except:
			pass
		if not event:
			event_serializer = EventSerializer(data=item)
			event_serializer.is_valid()
			event_serializer.save()
			return event_serializer.data['id']
		else:
			event.name = item['name']
			event.date = item['date']
			event.save()
			return event.id


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-k', '--kind', type=str, required=True, help="determine either event or bout. e.g. python3 newscraper.py -k event")
	kind = parser.parse_args().kind

	scraper = Scraper()
	if kind == 'event':
		scraper.start_events()
	elif kind == 'bout':
		scraper.start_bouts()

