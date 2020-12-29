from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Event(models.Model):
	STATUS_TYPE = [
		('upcoming', 'Upcoming'),
		('completed', 'Completed'),
	]

	name = models.CharField(max_length=100)
	location = models.CharField(max_length=200, blank=True, default='')
	date = models.DateField()
	status = models.CharField(choices=STATUS_TYPE, max_length=50, blank=True, default='upcoming')
	detail_link = models.CharField(max_length=500, blank=True, default='')

	class Meta:
		ordering = ['date']

	def __str__(self):
		return "%s" % self.name

class Fighter(models.Model):
	name = models.CharField(max_length=100, blank=False, default='')
	title = models.CharField(max_length=100, blank=True, default='')

	def __str__(self):
		return "%s" % self.name

class Bout(models.Model):
	STATUS_TYPE = [
		('pending', 'Pending'),
		('completed', 'Completed'),
		('drawn', 'Drawn'),
	]

	fighter1 = models.ForeignKey(
		Fighter,
		on_delete=models.CASCADE,
		related_name='fighter1s'
	)

	fighter2 = models.ForeignKey(
		Fighter,
		on_delete=models.CASCADE,
		related_name='fighter2s',
	)

	winner = models.ForeignKey(
		Fighter,
		on_delete=models.CASCADE,
		related_name='winners',
		default=None,
		blank=True,
		null=True
	) 

	loser = models.ForeignKey(
		Fighter,
		on_delete=models.CASCADE,
		related_name='losers',
		default=None,
		blank=True,
		null=True
	) 

	event = models.ForeignKey(
		Event,
		related_name='bout_events', 
		on_delete=models.CASCADE,
	)

	status = models.CharField(choices=STATUS_TYPE, max_length=50, blank=True, default='pending')
	weight_class = models.CharField(max_length=50, blank=True, default='')
	method = models.CharField(max_length=100, blank=True, default='')
	round = models.CharField(max_length=20, blank=True, default=1)
	time = models.CharField(max_length=20, blank=True, default='00:00')
	detail_link = models.CharField(max_length=500, blank=True, default='')

	def __str__(self):
		return "%s vs. %s" % (self.fighter1, self.fighter2)

class Entry(models.Model):
	event = models.ForeignKey(
		Event,
		related_name='entry_events', 
		on_delete=models.CASCADE,
	)
	user = models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		related_name='users',
	)

	def __str__(self):
		return "%s - %s" % (self.user, self.event)

class SelectionManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

class Selection(models.Model):
	bout = models.ForeignKey(
		Bout,
		related_name='bouts', 
		on_delete=models.CASCADE,
	)
	fighter = models.ForeignKey(
		Fighter,
		on_delete=models.CASCADE,
		related_name='fighters',
	) 
	entry = models.ForeignKey(
		Entry,
		related_name="entries",
		on_delete=models.CASCADE
	)

	# objects = SelectionManager()
	# Indicate whether the user won the contest based upon the bout result
	# 1: winner 0: loser
	# status = models.BooleanField(default=False, null=True, blank=True)
	# Indicate whether the bout has finished
	# finished = models.BooleanField(default=False, null=True, blank=True)

	def __str__(self):
		return "%s - %s" % (self.bout, self.fighter)


