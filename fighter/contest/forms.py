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
			if cleaned_data["type_of_registration"] == 'private':
				return cleaned_data
			else:
				games = (
					Game.objects.filter(event=event)
					.filter(type_of_registration="public")
					.filter(buyin=0)
				)
				if self.instance.id:
					if games and games.first().id == self.instance.id:
						return cleaned_data
					raise MainGameExistException()
				else:
					if games.count():
						raise MainGameExistException()
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
