from django.contrib.auth.models import Group
from contest.models import (
	Event,
	Bout,
	Fighter,
	Selection,
	Entry,
	CustomUser,
	ChatRoom,
	ChatFile,
	ChatMessage
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
	avatar = serializers.CharField(
		required=False,
		max_length=500,
	)

	def get_cleaned_data(self):
		data_dict = super().get_cleaned_data()
		data_dict['displayname'] = self.validated_data.get('displayname', '')
		data_dict['avatar'] = self.validated_data.get('avatar', '')
		return data_dict

class UserSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = CustomUser
		fields = ['id', 'username', 'displayname', 'email', 'avatar']


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

# Chat

class ChatRoomSerializer(serializers.ModelSerializer):
	class Meta:
		model = ChatRoom
		fields = '__all__'

class ChatFileSerializer(serializers.ModelSerializer):
	class Meta:
		model = ChatFile
		fields = '__all__'

class ChatMessageSerializer(serializers.ModelSerializer):
	class Meta:
		model = ChatMessage
		fields = '__all__'


