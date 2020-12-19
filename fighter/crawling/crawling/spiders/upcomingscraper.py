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
	FighterSerializer,
	EntrySerializer
)
from contest.util import _valid, convert_date, strip_list1

class ScraperSpider(scrapy.Spider):
	name = 'scraper'
	allowed_domains = ['ufcstats.com']
	start_urls = ['http://ufcstats.com/statistics/events/upcoming']

	def start_requests(self):
		# upcoming events
		yield scrapy.Request(self.start_urls[0], dont_filter=True, callback=self.parse_event)

		# scan db to get the scraped events to get the stats
		events = Event.objects.all()
		for event in events:
			yield scrapy.Request(event.detail_link, meta={'event_id': event.id}, callback=self.parse_event_detail)

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
				event_id = self.save_event(item)

				yield scrapy.Request(detail_link, meta={'event_id': event_id}, callback=self.parse_event_detail)

	def parse_event_detail(self, response):
		event_id = response.meta['event_id']
		event = Event.objects.get(pk=event_id)
		trs = response.css('table.b-fight-details__table tr.b-fight-details__table-row')
		if trs:
			for tr in trs[1:]:
				fight_detail = _valid(tr.xpath('.//td[1]//text()').get())
				detail_link = tr.xpath('@data-link').get()
				fighters = strip_list1(tr.xpath('.//td[2]/p/a/text()').getall())
				weight_class = _valid(tr.xpath('.//td[7]/p/text()').get())

				item = dict(
					fighter1=self.save_fighter({'name': fighters[0]}).id,
					fighter2=self.save_fighter({'name': fighters[1]}).id,
					weight_class=weight_class,
					detail_link=detail_link,
					status='pending',
					event=event
				)
				bout = self.save_bout(item)

				if fight_detail:
					event.update(status='completed')

				yield scrapy.Request(detail_link, meta={'bout_id': bout.id}, callback=self.parse_bout_detail)

	def parse_bout_detail(self, response):
		bout_id = response.meta['bout_id']
		bout = Bout.objects.get(pk=bout_id)

		persons = response.css('div.b-fight-details__person')
		for person in persons:
			not_yet_finished = person.css('i.b-fight-details__person-status_style_none')
			if not not_yet_finished:
				bout.update(status='completed')

			marks = _valid(person.css('i::text').get())
			name = _valid(person.css('div.b-fight-details__person-text h3 a::text').get())
			title = _valid(person.css('div.b-fight-details__person-text p.b-fight-details__person-title::text').get())
			if marks: # bout finished
				fighter = self.get_fighter(name)
				if fighter:
					entries = Entry.filter(bout_id=fighter.id)
					entries.update(finished=True)
					for entry in entries:
						status = False
						if entry.fighter_id == fighter.id:
							status = True
						entry.update(statue=status)

				if marks == 'W':
					bout.winner = fighter
				elif marks == 'L':
					bout['loser'] = fighter
				elif marks == 'D':
					bout.update(status='drawn')

			self.update_fighter_in_bout(bout, name, title.replace('"', ''))

	def get_fighter(name):
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
		try:
			bout = Bout.objects.get(detail_link=item['detail_link'])
		except:
			pass
		if not bout:
			bout_serializer = BoutSerializer(data=item)
			if bout_serializer.is_valid():
				bout = bout_serializer.save()

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
			return event_serializer.data()['id']
		else:
			return event.id

	

