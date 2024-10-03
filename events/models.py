from datetime import timedelta
import base62
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext as _
from utils.snowflake_id_generator import SnowflakeIDGeneratorSingleton


def generate_snowflake_id():
    return base62.encode(SnowflakeIDGeneratorSingleton().get_snowflake_id())


class EventType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class EventType(models.TextChoices):
    ONE_OFF = 'OF', _('One-Off')
    ONE_ON_ONE = 'OO', _('One-on-One')


class EventOccurrenceType(models.TextChoices):
    BETWEEN_DATES = 'BD', _('Between 2 dates')
    LIST_OF_DATES = 'LD', _('List of Dates')
    RECURRING = 'RE', _('Recurring')


class Event(models.Model):
    id = models.CharField(primary_key=True, max_length=22, default=generate_snowflake_id, editable=False)
    name = models.CharField(max_length=200)
    event_type = models.CharField(
        max_length=2,
        choices=EventType.choices,
        default=EventType.ONE_ON_ONE,
    )
    event_occurrence_type = models.CharField(
        max_length=2,
        choices=EventOccurrenceType.choices,
        default=EventOccurrenceType.BETWEEN_DATES,
    )
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    duration = models.IntegerField(default=30)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event_dates = models.JSONField(default=list, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

