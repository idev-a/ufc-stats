# Generated by Django 3.1 on 2021-03-27 08:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0044_game_teams_limit'),
    ]

    operations = [
        migrations.RenameField(
            model_name='game',
            old_name='teams_limit',
            new_name='entry_limit',
        ),
    ]
