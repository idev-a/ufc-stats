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


class GameManager(models.Manager):
 
    def get_games(self, event, user_id=None):
        games = [dict(
            name=event.name,
            group='Single',
            event_id=event.id,
            date=event.date,
            joined_users=0,
            value=-1,
            genre='free',
            buyin=0,
            added_prizepool=0,
            prize=0,
            action=event.action,
            re_entry=False,
            multientry=1
        )]

        if user_id:
            multi_games = self.filter(joined_users__pk=user_id).filter(~Q(event__action='completed'))
            if multi_games:
                for _ in multi_games:
                    games.append(dict(
                        name=_.name,
                        group='Multiple',
                        date=_.date,
                        value=_.id,
                        event_id=_.event.id,
                        instructions=_.instructions,
                        summary=_.summary,
                        rules_set=_.rules_set,
                        action=_.action,
                        genre=_.genre,
                        buyin=_.buyin,
                        prize=_.prize,
                        joined_users=_.joined_users.count(),
                        added_prizepool=_.added_prizepool,
                        re_entry=_.re_entry,
                        multientry=_.multientry
                    ))

        return games

class EntryManager(models.Manager):

   def get_total_winners(self, game_id):
        entries = self.filter(game_id=game_id)
        total = 0
        for _ in entries:
            if _.ranking == 1:
                total += 1
        return total