from django.db import models
from django.utils import timezone
from django.core.validators import MinLengthValidator, MaxValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractUser
from django.template.defaultfilters import truncatewords  # or 

from .managers import CustomUserManager, GameManager, EntryManager

import pdb

ACTION_TYPE = [
	('started', 'Started'),
	('completed', 'Completed'),
]

# Customize User model
class CustomUser(AbstractUser):
	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = []

	objects = CustomUserManager()

	displayname = models.CharField(blank=True, null=True, max_length=100, unique=True, validators=[MinLengthValidator(3)])
	avatar = models.CharField(blank=True, null=True, max_length=500)
	first_name = models.CharField(blank=True, null=True, max_length=100)
	last_name = models.CharField(blank=True, null=True, max_length=100)
	coins = models.PositiveIntegerField(blank=True, null=True, default=1000)
	referred_by = models.ForeignKey(
		'self',
		on_delete=models.CASCADE,
		related_name='referrals',
		default=None,
		blank=True,
		null=True
	)

	@property
	def initials(self):
		name_list = (self.displayname or 'Unknown').split()

		_initials = ""

		for name in name_list:  # go through each name
			_initials += name[0].upper()  # append the initial

		if len(_initials) > 2:
			return _initials[:2]
		return _initials


	def __str__(self):
		return self.email or self.username

# Create your models here.
class Event(models.Model):
	STATUS_TYPE = [
		('upcoming', 'Upcoming'),
		('old', 'Old'),
	]

	name = models.CharField(max_length=100)
	location = models.CharField(max_length=200, blank=True, default='')
	date = models.DateTimeField()
	status = models.CharField(choices=STATUS_TYPE, max_length=50, blank=True, default='upcoming')
	action = models.CharField(choices=ACTION_TYPE, max_length=50, blank=True)
	detail_link = models.URLField(max_length=500, blank=True, default='')

	class Meta:
		ordering = ['-date']

	def __str__(self):
		return "%s (%s)" % (self.name, self.date.strftime('%Y-%m-%d'))

class Fighter(models.Model):
	name = models.CharField(max_length=100, blank=False, default='')
	title = models.CharField(max_length=100, blank=True, default='')

	def __str__(self):
		return "%s" % self.name

class Notification(models.Model):
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
	round = models.PositiveIntegerField(blank=True, null=True, default=1)
	time = models.CharField(max_length=20, blank=True, default='00:00')
	go_the_distance = models.BooleanField(null=True, blank=True)
	detail_link = models.URLField(max_length=500, blank=True, default='')

	def __str__(self):
		return "%s vs. %s" % (self.fighter1, self.fighter2)


# multiple games
class Game(models.Model):
	REGISTRATION_TYPES = [
		('private', 'Private'),
		('public', 'Public')
	]

	GENRE_TYPES = [
		('free', 'Free'),
		('paid', 'Paid')
	]

	owner = models.ForeignKey(
		CustomUser,
		on_delete=models.CASCADE,
		related_name='game_owners',
		default=None,
	)

	event = models.ForeignKey(
		Event,
		related_name='game_event', 
		on_delete=models.CASCADE,
	)

	objects = GameManager()

	name = models.CharField(max_length=100, blank=False, default='')
	type_of_registration = models.CharField(choices=REGISTRATION_TYPES, max_length=50, blank=True, default='public')
	entrants = models.ManyToManyField(CustomUser, blank=True, related_name='game_entrants')
	joined_users = models.ManyToManyField(CustomUser, blank=True, related_name='game_joined_users')
	instructions = models.TextField(default='', max_length=500, blank=False)
	rules_set = models.TextField(default='', max_length=500, blank=False)

	# Determine where game is free to play or needs some coins to join.
	genre = models.CharField(choices=GENRE_TYPES, max_length=20, blank=True, default='free')
	
	'''
		the first one is kind of free game in which any one is free to join 
		and the winner will get fixed buyin by admin.
		On the other hands, for the paid game the user is asked to pay coin to join, 
		but the winner will get higher coins 
		which will be sum of all buyin of joined users plus one by admin.
	'''
	buyin = models.PositiveIntegerField(blank=True, null=True, default=0)

	# Added by Admin
	buyin_bonus = models.PositiveIntegerField(blank=True, null=True, default=0)

	@property
	def date(self):
		return self.event.date

	@property
	def action(self):
		return self.event.action

	@property
	def prize(self):
		_prize = 0
		if self.genre == 'paid':
			_prize = self.joined_users.count() * self.buyin + self.buyin_bonus
		return _prize
	
	def info_entrants(self):
		return '{}'.format(self.entrants.count())

	def info_joined(self):
		return '{}'.format(self.joined_users.count())

	@property
	def short_instructions(self):
		return truncatewords(self.instructions, 50)

	@property
	def short_rules_set(self):
		return truncatewords(self.rules_set, 50)

	info_entrants.short_description  = 'Total entrants'
	info_joined.short_description  = 'Total joined users'

	def __str__(self):
		return "%s - %s(%s)" % (self.event, self.entrants.count(), self.joined_users.count())

class Entry(models.Model):
	event = models.ForeignKey(
		Event,
		related_name='entry_events', 
		on_delete=models.CASCADE,
	)
	user = models.ForeignKey(
		CustomUser,
		on_delete=models.CASCADE,
		related_name='users',
	)
	game = models.ForeignKey(
		Game,
		on_delete=models.CASCADE,
		related_name='entry_games',
		default=None,
		blank=True,
		null=True
	)

	objects = EntryManager()

	last_edited = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	# last_edited.editable=True
	ranking = models.IntegerField(blank=True, null=True, default=0)

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
	survivor1 = models.ForeignKey(
		Fighter,
		on_delete=models.CASCADE,
		related_name='survivor1s',
		default=None,
		blank=True,
		null=True
	)
	survivor2 = models.ForeignKey(
		Fighter,
		on_delete=models.CASCADE,
		related_name='survivor2s',
		default=None,
		blank=True,
		null=True
	) 
	entry = models.ForeignKey(
		Entry,
		related_name="entries",
		on_delete=models.CASCADE
	)

	def __str__(self):
		return "%s - %s (%s)" % (self.survivor1, self.survivor2, self.bout)

# Chat
class ChatRoom(models.Model):
	avatar = models.CharField(max_length=500, default="room_avatar.jpg", blank=True, null=True)
	name = models.CharField(max_length=50)
	users = ArrayField(models.PositiveIntegerField(blank=True))
	last_updated = models.DateTimeField(null=True, blank=True)

	def __str__(self):
		return f'{self.name}({len(self.users)})'

class ChatFile(models.Model):
	name = models.CharField(max_length=50)
	size = models.PositiveIntegerField()
	type = models.CharField(max_length=50)
	extension = models.CharField(max_length=50)
	url = models.CharField(max_length=500)

	def __str__(self):
		return f'{self.name}.{self.extension}({type})'

class ChatMessage(models.Model):
	room = models.ForeignKey(
		ChatRoom,
		related_name="chat_rooms",
		on_delete=models.CASCADE
	)
	sender = models.ForeignKey(
		CustomUser,
		related_name="senders",
		on_delete=models.CASCADE
	)
	file = models.ForeignKey(
		ChatFile,
		related_name="chat_files",
		on_delete=models.CASCADE,
		default=None,
		blank=True,
		null=True
	)
	reply_message = models.ForeignKey(
		'self',
		related_name="chat_messages",
		on_delete=models.CASCADE,
		default=None,
		blank=True,
		null=True
	)
	content = models.TextField(default='', blank=True, null=True)
	timestamp = models.DateTimeField(null=True, blank=True)
	new = models.BooleanField(null=True, blank=True)
	system = models.BooleanField(null=True, blank=True)
	saved = models.BooleanField(null=True, blank=True)
	seen = models.BooleanField(null=True, blank=True)
	distributed = models.BooleanField(null=True, blank=True)
	disable_actions = models.BooleanField(null=True, blank=True)
	disable_reactions = models.BooleanField(null=True, blank=True)
	deleted = models.DateTimeField(null=True, blank=True)
	edited = models.DateTimeField(null=True, blank=True)

	def __str__(self):
		cnt = len(self.content) or 0
		return f'{self.content[:cnt]} {self.timestamp}'



