# Generated by Django 3.1 on 2021-02-26 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0024_game_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='action',
            field=models.CharField(blank=True, choices=[('started', 'Started'), ('completed', 'Completed')], max_length=50),
        ),
    ]