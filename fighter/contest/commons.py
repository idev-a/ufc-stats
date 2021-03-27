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

def get_games(event, user_id=None):
	public_games = Game.objects.filter(event=event).filter(type_of_registration='public')
	games = []
	if public_games:
		event_data = EventSerializer(event).data
		for _ in public_games:
			games.append(dict(
				id=_.id,
				name=_.name,
				group='single',
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

		if user_id:
			multi_games = Game.objects.filter(joined_users__pk=user_id).filter(event=event).exclude(pk=_.id).exclude(type_of_registration='public')
			if multi_games:
				for _ in multi_games:
					games.append(dict(
						id=_.id,
						name=_.name,
						group='Multiple',
						date=_.date,
						value=_.id,
						event=event_data,
						type_of_registration=_.type_of_registration,
						instructions=_.instructions,
						summary=_.summary,
						rules_set=_.rules_set,
						action=_.action,
						entry_limit=_.entry_limit,
						genre=_.genre,
						buyin=_.buyin,
						prize=_.prize,
						entrants=UserSerializer(_.entrants, many=True).data,
						joined_users=UserSerializer(_.joined_users, many=True).data,
						added_prizepool=_.added_prizepool,
						re_entry=_.re_entry,
						multientry=_.multientry
					))

	return games

def load_my_games(event, user_id=None):
	public_games = Game.objects.filter(event=event).filter(type_of_registration='public')
	games = []
	if public_games:
		event_data = EventSerializer(event).data
		for _ in public_games:
			games.append(dict(
				id=_.id,
				name=_.name,
				group='single',
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

		if user_id:
			multi_games = Game.objects.filter(entrants__pk=user_id).filter(event=event).exclude(pk=_.id).exclude(type_of_registration='public')
			if multi_games:
				for _ in multi_games:
					games.append(dict(
						id=_.id,
						name=_.name,
						group='Multiple',
						date=_.date,
						value=_.id,
						event=event_data,
						type_of_registration=_.type_of_registration,
						instructions=_.instructions,
						summary=_.summary,
						rules_set=_.rules_set,
						action=_.action,
						entry_limit=_.entry_limit,
						genre=_.genre,
						buyin=_.buyin,
						prize=_.prize,
						entrants=UserSerializer(_.entrants, many=True).data,
						joined_users=UserSerializer(_.joined_users, many=True).data,
						added_prizepool=_.added_prizepool,
						re_entry=_.re_entry,
						multientry=_.multientry
					))

	return games

def create_main_contest(event):
	game = Game(name='Main Contest', event=event, added_prizepool=100, buyin=0)
	game.save()
