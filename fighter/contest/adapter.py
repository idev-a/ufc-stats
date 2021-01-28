from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter
from contest.models import CustomUser

class MyAccountAdapter(DefaultAccountAdapter):

	def save_user(self, request, user, form, commit=False):
		user = super().save_user(request, user, form, commit)
		data = form.cleaned_data
		print(data)
		user.displayname = data.get('displayname')
		user.avatar = data.get('avatar')
		referred_by = None
		if data.get('referred_by'):
			try:
				referred_by = CustomUser.objects.get(pk=data.get('referred_by'))
			except Exception as err:
				print(err)
		if referred_by:
			user.referred_by = referred_by
		user.save()
		return user