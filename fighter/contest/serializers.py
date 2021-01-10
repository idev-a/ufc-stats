from django.contrib.auth.models import Group
from contest.models import (
	Event,
	Bout,
	Fighter,
	Selection,
	Entry,
	CustomUser
)
from rest_framework import serializers

from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email

from rest_auth.registration.serializers import RegisterSerializer

class CustomRegisterSerializer(RegisterSerializer):
	displayname = serializers.CharField(
		required=False,
		max_length=100,
	)

	def get_cleaned_data(self):
		data_dict = super().get_cleaned_data()
		data_dict['displayname'] = self.validated_data.get('displayname', '')
		return data_dict

class UserSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = CustomUser
		fields = ['id', 'url', 'username', 'displayname', 'email']


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


