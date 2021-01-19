from django.db.models.sql import datastructures
from django.core.exceptions import EmptyResultSet

datastructures.EmptyResultSet = EmptyResultSet

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from fighter.celery import app as celery_app
from contest.tasks import countdown

__all__ = ('celery_app',)

countdown.delay()