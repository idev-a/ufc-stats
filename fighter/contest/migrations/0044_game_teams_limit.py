# Generated by Django 3.1 on 2021-03-26 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0043_auto_20210326_0229'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='teams_limit',
            field=models.PositiveIntegerField(blank=True, default=10, null=True),
        ),
    ]
