# Generated by Django 3.1 on 2021-04-08 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0002_auto_20210408_0233'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='bouts',
            field=models.ManyToManyField(blank=True, related_name='game_bouts', to='contest.Bout'),
        ),
    ]
