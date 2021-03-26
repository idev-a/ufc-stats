from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.db.models import Q

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, username, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not username:
            raise ValueError(_('The username must be set'))
        # email = self.normalize_email(email)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):
        """
        Create and save a SuperUser with the given username and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(username, password, **extra_fields)

class EventManager(models.Manager):
    
    def latest_event(self):
        events = self.filter(status='upcoming')
        event = None
        if events:
            event = events.latest('-date')
        return event

# class GameManager(models.Manager):
#     def main_contest():
#         from contest.models import Game, Event
#         return self.filter(event=Event.objects.latest_event()).filter(buyin=0).filter(type_of_registration='public').first()


class EntryManager(models.Manager):

   def get_total_winners(self, game_id):
        entries = self.filter(game_id=game_id)
        total = 0
        for _ in entries:
            if _.ranking == 1:
                total += 1
        return total