import requests
from scrapy.selector import Selector
import pdb

class Scaper:
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

	def run(self):
		self.scrape_events()

		self.scrape_event_detail()

		self.scrape_bout()

	def scrape_events(self):
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
					date=date,
					location=location,
					detail_link=detail_link,
					status='upcoming'
				))

	def scrape_bout(self):
		pdb.set_trace()
		for bout in self.bouts:
			res = self.session.get(bout['fight_detail_link']).content
			response = Selector(text=res)
			persons = response.css('div.b-fight-details__person')


	def scrape_event_detail(self):
		pdb.set_trace()
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
						fighters=fighters,
						weight_class=weight_class,
						fight_detail_link=fight_detail_link
					))

					if fight_detail:
						event['status'] = 'completed'


if __name__ == '__main__':
	scraper = Scaper()

	scraper.run()