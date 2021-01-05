import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "."))
os.environ['DJANGO_SETTINGS_MODULE'] = 'fighter.settings'
import django
django.setup()

from scrapy.crawler import CrawlerProcess
import scrapy
import pdb

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

class ScraperSpider(scrapy.Spider):
	name = 'scraper'
	allowed_domains = ['ufcstats.com']
	# start_urls = ['http://ufcstats.com/statistics/events/upcoming']
	start_urls = ['http://ufcstats.com/statistics/events/completed']

	def start_requests(self):
		# upcoming events
		# yield scrapy.Request(self.start_urls[0], dont_filter=True, callback=self.parse_event)

		# scan db to get the scraped events to get the stats
		events = Event.objects.all()
		for event in events:
			yield scrapy.Request(event.detail_link, dont_filter=True, meta={'event_id': event.id}, callback=self.parse_event_detail)

	def parse_event(self, response):
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

				if detail_link == 'http://ufcstats.com/event-details/307064d3e0f036c2':
					continue

				event_id = self.save_event(item)

				yield scrapy.Request(detail_link, dont_filter=True, meta={'event_id': event_id}, callback=self.parse_event_detail)

	def parse_event_detail(self, response):
		event_id = response.meta['event_id']
		event = Event.objects.get(pk=event_id)
		trs = response.css('table.b-fight-details__table tr.b-fight-details__table-row')
		if trs:
			for tr in trs[1:]:
				fight_detail = strip_list1(tr.xpath('.//td[1]//text()').getall())
				detail_link = tr.xpath('@data-link').get()
				fighters = strip_list1(tr.xpath('.//td[2]/p/a/text()').getall())
				weight_class = _valid(tr.xpath('.//td[7]/p/text()').get())
				method = _valid(' '.join(strip_list1(tr.xpath('.//td[8]//text()').getall())))
				go_the_distance = True if 'dec' in _valid(method) else False
				round = _valid(tr.xpath('.//td[9]/p/text()').get())
				time = _valid(tr.xpath('.//td[10]/p/text()').get())

				item = dict(
					fighter1=self.save_fighter({'name': fighters[0]}).id,
					fighter2=self.save_fighter({'name': fighters[1]}).id,
					weight_class=weight_class,
					method=method,
					round=round,
					time=time,
					go_the_distance=go_the_distance,
					detail_link=detail_link,
					status='pending',
					event=event.id
				)
				bout = self.save_bout(item)

				if fight_detail:
					event.status='completed'
					event.save()

				try:
					yield scrapy.Request(detail_link, dont_filter=True, meta={'bout_id': bout.id}, callback=self.parse_bout_detail)
				except:
					pass

	def parse_bout_detail(self, response):
		bout_id = response.meta['bout_id']
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
    process = CrawlerProcess(settings={
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1',
        "CONCURRENT_REQUESTS": "16",
        "DOWNLOAD_DELAY": ".5",
    })

    process.crawl(ScraperSpider)
    process.start() # the script will block here until the crawling is finished	

