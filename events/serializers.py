from rest_framework import serializers
from .models import Event, EventType, EventOccurrenceType


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'name', 'active', 'event_type', 'start_date', 'end_date', 'duration', 'event_occurrence_type',
                  'event_dates', 'recurring_event_time', 'description', 'location', 'created_at', 'updated_at']

    def validate(self, data):
        event_occurrence_type = data.get('event_occurrence_type')
        event_type = data.get('event_type')
        if event_type == EventType.ONE_OFF:
            if not isinstance(data.get('event_dates'), list) or not all(
                    isinstance(item, dict) and 'date' in item and 'time_keys' in item for item in
                    data.get('event_dates')):
                raise serializers.ValidationError(
                    "For ONE_OFF event type, event_dates must be a list of dicts with 'date' and 'time_keys'.")
        elif event_type == EventType.ONE_ON_ONE:
            if event_occurrence_type == EventOccurrenceType.RECURRING:
                if not data.get('recurring_event_time') or not isinstance(data.get('event_dates'), list):
                    raise serializers.ValidationError(
                        "For ONE_ON_ONE, Recurring event type, event_dates must be a list of dicts with 'date'.")

            elif event_occurrence_type == EventOccurrenceType.BETWEEN_DATES:
                if not data.get('start_date') or not data.get('end_date'):
                    raise serializers.ValidationError(
                        "start_date and end_date are mandatory for BETWEEN_DATES and RECURRING event types.")
            elif event_occurrence_type == EventOccurrenceType.LIST_OF_DATES:
                if not data.get('event_dates'):
                    raise serializers.ValidationError("event_dates are mandatory for LIST_OF_DATES event type.")
        return data


class EventBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ["event_id", "attendee_email", "status", "created_at"]