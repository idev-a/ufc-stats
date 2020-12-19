import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "."))
os.environ['DJANGO_SETTINGS_MODULE'] = 'fighter.settings'
import django
django.setup()

import requests
from scrapy.selector import Selector
from datetime import datetime
import pdb

from contest.models import Event
from contest.serializers import EventSerializer
from logger import logger

class Scraper:
	name = "ufc"
	start_urls = ["http://ufcstats.com/statistics/events/completed"]
	events = []
	bouts = []

	def __init__(self):
		self.session = requests.Session()

	def _valid(self, val):
		if val:
			return val.strip()
		else:
			return ''

	def strip_list1(self, arr):
		new_list = []
		for item in arr:
			if item:
				new_list.append(self._valid(item))
			else:
				new_list.append(' ')

		return new_list

	def convert_date(self, date):
		return datetime.strptime(date, '%B %d, %Y').strftime('%Y-%m-%d')

	def run(self):
		self.scrape_upcoming_events()

		self.scrape_past_events_from_db()

		self.save_data()

	def save_data(self):
		pdb.set_trace()
		event_serializer = EventSerializer(data=self.events, many=True)
		event_serializer.is_valid()
		event_serializer.save()

	def scrape_past_events_from_db(self):
		pass

	def scrape_upcoming_events(self):
		self.scrape_events()

		# self.scrape_event_detail()

		# self.scrape_bout()

	def scrape_events(self):
		logger.info('Scraping event')
		res = self.session.get('http://ufcstats.com/statistics/events/upcoming').content
		response = Selector(text=res)
		trs = response.css('table.b-statistics__table-events tr.b-statistics__table-row')
		if len(trs) > 2:
			for tr in trs[2:]:
				name = self._valid(tr.css('a::text').get())
				detail_link = self._valid(tr.css('a').xpath('@href').get())
				location = self._valid(tr.xpath('.//td[2]/text()').get())
				date = self._valid(tr.css('span.b-statistics__date::text').get())

				self.events.append(dict(
					name=name,
					date=self.convert_date(date),
					location=location,
					detail_link=detail_link,
					status='upcoming'
				))

	def scrape_bout(self):
		logger.info('Scraping bout detail')
		for bout in self.bouts:
			res = self.session.get(bout['fight_detail_link']).content
			response = Selector(text=res)
			persons = response.css('div.b-fight-details__person')
			x = 1
			for person in persons:
				not_yet_finished = person.css('i.b-fight-details__person-status_style_none')
				if not not_yet_finished:
					bout['status'] = 'completed'

				marks = self._valid(person.css('i::text').get())
				name = self._valid(person.css('div.b-fight-details__person-text h3 a::text').get())
				title = self._valid(person.css('div.b-fight-details__person-text p.b-fight-details__person-title::text').get())
				if marks == 'W':
					bout['winner'] = name
				elif marks == 'L':
					bout['loser'] = name
				elif marks == 'D':
					bout['status'] == 'drawn'

				title_idx = f'fighter{x}_title'
				bout[title_idx] = title.replace('"', '')

				x += 1

		# print(self.bouts)

	def scrape_event_detail(self):
		logger.info('Scraping event detail')
		for event in self.events:
			res = self.session.get(event['detail_link']).content
			response = Selector(text=res)
			trs = response.css('table.b-fight-details__table tr.b-fight-details__table-row')
			if trs:
				for tr in trs[1:]:
					fight_detail = self._valid(tr.xpath('.//td[1]//text()').get())
					fight_detail_link = tr.xpath('@data-link').get()
					fighters = self.strip_list1(tr.xpath('.//td[2]/p/a/text()').getall())
					weight_class = self._valid(tr.xpath('.//td[7]/p/text()').get())

					self.bouts.append(dict(
						fighter1_name=fighters[0],
						fighter2_name=fighters[1],
						weight_class=weight_class,
						fight_detail_link=fight_detail_link,
						winner='',
						logger='',
						status='pending'
					))

					if fight_detail:
						event['status'] = 'completed'


if __name__ == '__main__':
	scraper = Scraper()

	scraper.run()