from django.contrib.auth.models import Group
from contest.models import (
	Event,
	Bout,
	Fighter,
	Selection,
	Entry,
	Game,
	CustomUser,
	ChatRoom,
	ChatFile,
	ChatMessage,
	Faq,
	Ticket
)
from rest_framework import serializers
from rest_flex_fields import FlexFieldsModelSerializer

from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email

from rest_auth.registration.serializers import RegisterSerializer

import pdb

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = CustomUser
		fields = ['id', 'username', 'displayname', 'email', 'coins', 'initials', 'avatar', 'referred_by', 'date_joined']


class CustomRegisterSerializer(RegisterSerializer):
	displayname = serializers.CharField(
		required=False,
		max_length=100,
	)
	avatar = serializers.CharField(
		required=False,
		max_length=500,
	)

	referred_by = serializers.IntegerField(
		required=False,
	)

	def get_cleaned_data(self):
		data_dict = super().get_cleaned_data()
		data_dict['displayname'] = self.validated_data.get('displayname', '')
		data_dict['avatar'] = self.validated_data.get('avatar', '')
		data_dict['referred_by'] = self.validated_data.get('referred_by', '')
		return data_dict

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

class GameSerializer(serializers.ModelSerializer):
	class Meta:
		model = Game
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

class ChatMessageSerializer(FlexFieldsModelSerializer):
	class Meta:
		model = ChatMessage
		fields = '__all__'
		expandable_fields = {
          'reply_message': ('contest.ChatMessageSerializer')
        }

# FAQ

class FaqSerializer(serializers.ModelSerializer):
	class Meta:
		model = Faq
		fields = '__all__'

class TicketSerializer(serializers.ModelSerializer):
	class Meta:
		model = Ticket
		fields = '__all__'