# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from contest.models import Event
from contest.serializers import EventSerializer
import pdb

class CrawlingPipeline:
	def process_item(self, item, spider):
		event_serializer = EventSerializer(data=item)
		event_serializer.is_valid()
		return item
