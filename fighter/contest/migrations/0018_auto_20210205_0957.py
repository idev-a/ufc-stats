# Generated by Django 3.1 on 2021-02-05 17:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0017_auto_20210205_0122'),
    ]

    operations = [
        migrations.RenameField(
            model_name='entry',
            old_name='rank',
            new_name='ranking',
        ),
    ]
