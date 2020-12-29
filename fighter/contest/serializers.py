from django.contrib.auth.models import User, Group
from contest.models import (
	Event,
	Bout,
	Fighter,
	Selection,
	Entry
)
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = User
		fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Group
		fields = ['url', 'name']

class FighterSerializer(serializers.ModelSerializer):
	class Meta:
		model = Fighter
		fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
	class Meta:
		model = Event
		fields = '__all__'

class BoutSerializer(serializers.ModelSerializer):
	class Meta:
		model = Bout
		fields = '__all__'

class SelectionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Selection
		fields = '__all__'

class EntrySerializer(serializers.ModelSerializer):
	class Meta:
		model = Entry
		fields = '__all__'


