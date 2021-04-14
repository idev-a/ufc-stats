DEFAULT_RULES_SET = [
  'User can pick any number of fighters. If any of them get finished, user is eliminated.',
  'Out of all surviving entries, the user with the most surviving fighters, wins the contest.',
  'If there is a tie, the winner is the entry with the most winning fighters.',
  'You are allowed to resubmit your team. 1 team per person.'
]

DEFAULT_INSTRUCTIONS = [
  'Choose fighters',
  'Hope they all survive'
]

WEIGHT_MAPPING = {
	'Strawweight': '115',
	'Flyweight': '125',
	'Bantamweight': '135',
	'Featherweight': '145',
	'Lightweight': '155',
	'Super Lightweight': '165',
	'Welterweight': '170',
	'Super Welterweight': '175',
	'Middleweight': '185',
	'Super Middleweight': '195',
	'Light Heavyweight': '205',
	'Cruiserweight': '225',
	'Heavyweight': '265',
	'Super Heavyweight': '265',
}

ROLE_CHOICES = (
	('user', 'User'),
	('admin', 'Admin'),
)

ACTION_TYPE = [
	('started', 'Started'),
	('completed', 'Completed'),
]

GENDER_TYPE = [
	('M', 'Male'),
	('F', 'Female'),
]

EVENT_STATUS_TYPE = [
	('upcoming', 'Upcoming'),
	('old', 'Old'),
]

BOUT_STATUS_TYPE = [
	('pending', 'Pending'),
	('completed', 'Completed'),
	('drawn', 'Drawn'),
]

TICKET_STATUS_TYPE = [
	('delivered', 'Delivered'),
	('resolved', 'Resolved'),
	('failed', 'Failed'),
]

REGISTRATION_TYPES = [
	('private', 'Private'),
	('public', 'Public')
]

GENRE_TYPES = [
	('free', 'Free'),
	('paid', 'Paid')
]
