# Generated by Django 3.1 on 2021-01-19 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0010_auto_20210115_1723'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='date',
            field=models.DateTimeField(),
        ),
    ]
