from django.conf import settings

from contest.models import (
	Event,
	Bout,
	Fighter,
	Selection,
	Entry,
	CustomUser,
	Game
)
from contest.serializers import (
	UserSerializer,
	GroupSerializer,
	EventSerializer,
	BoutSerializer,
	FighterSerializer,
	SelectionSerializer,
	EntrySerializer,
	GameSerializer
)

def main_contest():
	games = Game.objects.filter(event=Event.objects.latest_event()).filter(buyin=0).filter(type_of_registration='public')
	if games:
	    return games.first()
	else:
		return -1

def build_games(games, data, event_data):
	for _ in data:
		games.append(dict(
			id=_.id,
			name=_.name,
			group='no important',
			date=_.date,
			value=_.id,
			event=event_data,
			type_of_registration=_.type_of_registration,
			instructions=_.instructions,
			summary=_.summary,
			rules_set=_.rules_set,
			action=_.action,
			genre=_.genre,
			entry_limit=_.entry_limit,
			buyin=_.buyin,
			prize=_.prize,
			entrants=UserSerializer(_.entrants, many=True).data,
			joined_users=UserSerializer(_.joined_users, many=True).data,
			added_prizepool=_.added_prizepool,
			re_entry=_.re_entry,
			multientry=_.multientry
		))

def build_games_with_entry(games, data, event_data):
	for _ in data:
		for entry in range(1, (_.multientry or 1)+1):
			games.append(dict(
				id=_.id,
				name=_.name,
				group='no important',
				date=_.date,
				value=f"{_.id}_{entry}",
				event=event_data,
				type_of_registration=_.type_of_registration,
				instructions=_.instructions,
				summary=_.summary,
				rules_set=_.rules_set,
				action=_.action,
				genre=_.genre,
				entry_limit=_.entry_limit,
				buyin=_.buyin,
				prize=_.prize,
				entrants=UserSerializer(_.entrants, many=True).data,
				joined_users=UserSerializer(_.joined_users, many=True).data,
				added_prizepool=_.added_prizepool,
				re_entry=_.re_entry,
				multientry=_.multientry,
				entry_number=entry
			))

def get_games_with_entry(event, user_id=None):
	'''
		get games for selection
		For the private games, it will only games where user have already joined
		This will list the games based upon the entry
		e.g. Main Contest 
			 Private game (1)
			 Private game (2)
			 ...
	'''
	games = []
	event_data = EventSerializer(event).data
	public_games = Game.objects.filter(event=event).filter(type_of_registration='public')
	build_games_with_entry(games, public_games, event_data)

	if user_id:
		private_games = Game.objects.filter(joined_users__pk=user_id).filter(event=event).exclude(type_of_registration='public')
	build_games_with_entry(games, private_games, event_data)

	return games;

def get_games(event, user_id=None):
	'''
		get games for contest
		For the private games, it will only games where user have already joined
	'''
	public_games = Game.objects.filter(event=event).filter(type_of_registration='public')
	games = []
	event_data = EventSerializer(event).data
	build_games(games, public_games, event_data)

	if user_id:
		private_games = Game.objects.filter(joined_users__pk=user_id).filter(event=event).exclude(type_of_registration='public')
		build_games(games, private_games, event_data)

	return games

def load_my_games(event, user_id=None):
	'''
		load my games in lobby
		For the private games, it will all available games for user
	'''
	public_games = Game.objects.filter(event=event).filter(type_of_registration='public')
	games = []
	event_data = EventSerializer(event).data
	build_games(games, public_games, event_data)

	if user_id:
		private_games = Game.objects.filter(entrants__pk=user_id).filter(event=event).exclude(type_of_registration='public')
		build_games(games, private_games, event_data)

	return games

def create_main_contest(event):
	game = Game(name='Main Contest', event=event, added_prizepool=100, buyin=0)
	game.save()
