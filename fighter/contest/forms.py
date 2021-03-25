from django import forms
from django.core.exceptions import ValidationError
import pdb

from .models import Game
from .exceptions import MainGameExistException


class GameForm(forms.ModelForm):
	class Meta:
		model = Game
		fields = "__all__"

	# The clean method gets invoked before the GameAdmin's save_model method
	def clean(self):
		try:
			cleaned_data = super(GameForm, self).clean()
			event = cleaned_data["event"]
			games = (
				Game.objects.filter(event=event)
				.filter(type_of_registration="public")
				.filter(buyin=0)
			)
			if (
				games.count() > 1 or
				(cleaned_data["type_of_registration"] == "public"
				and cleaned_data["buyin"] == 0
				and games.first().event == event)
			):
				raise MainGameExistException()
			else:
				return cleaned_data
		except MainGameExistException:
			msg = "You've already created a default game for this event with the following conditions".format(event)
			raise ValidationError([
				ValidationError(msg),
				ValidationError(f'Type of Registration: Public'),
				ValidationError(f'Buyin: 0')
			])
		except Exception as err:
			print(err)
			raise ValidationError("")
