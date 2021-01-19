from celery import shared_task
import time
from datetime import datetime

@shared_task
def countdown():
	from contest.models import Event

	events = Event.objects.all().filter(status='upcoming')
	if events:
		_event = events.latest('-date')
		FMT = '%Y-%m-%d %H:%M:%S'
		_t = int(datetime.strptime(f'{_event.date} 17:00:00', FMT).timestamp() - datetime.now().timestamp())
		print(datetime.now(), _event.date, _t)
		while _t:
			print(f'[Countdown] {_t}')
			time.sleep(1)
			_t -= 1
		_event.action = 'started'
		_event.save()