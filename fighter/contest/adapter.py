from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter

import pdb

class MyAccountAdapter(DefaultAccountAdapter):

	def save_user(self, request, user, form, commit=False):
		user = super().save_user(request, user, form, commit)
		data = form.cleaned_data
		user.displayname = data.get('displayname')
		user.save()
		return user