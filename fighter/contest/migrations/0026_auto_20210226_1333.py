# Generated by Django 3.1 on 2021-02-26 21:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0025_auto_20210226_1307'),
    ]

    operations = [
        migrations.RenameField(
            model_name='game',
            old_name='date_started',
            new_name='date',
        ),
    ]
