# Generated by Django 3.1 on 2021-02-05 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0015_auto_20210205_0118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='rank',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
