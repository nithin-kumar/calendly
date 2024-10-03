import datetime
from datetime import timedelta

from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from scheduler.services import fetch_user_calendar, create_event
from utils.redis import RedisClientSingleton
from .models import Event, EventOccurrenceType, EventType
from .serializers import EventSerializer



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def events(request):
    serializer = EventSerializer(data=request.data)
    if serializer.is_valid():
        event_data = serializer.validated_data
        event, created = Event.objects.update_or_create(
            user=request.user,
            name=event_data['name'],
            start_date=event_data.get('start_date'),
            end_date=event_data.get('end_date'),
            duration=event_data.get('duration'),
            event_dates=event_data.get('event_dates'),
            defaults=event_data
        )
        event_url = f"{request.get_host()}/api/events/{event.id}/"
        return Response({"event": EventSerializer(event).data, "url": event_url}, status=201 if created else 200)
    return Response(serializer.errors, status=400)


@api_view(['GET'])
def handle_event(request, id):
    event = Event.objects.get(id=id)
    return Response({"event": EventSerializer(event).data}, status=200)


@api_view(['GET'])
def calendar_days_for_event(request, id):
    try:
        event = Event.objects.get(id=id)
    except Event.DoesNotExist:
        return Response({"error": "Event not found"}, status=404)

    if event.event_occurrence_type == EventOccurrenceType.RECURRING:
        date_list = event.event_dates
    elif event.event_occurrence_type == EventOccurrenceType.BETWEEN_DATES:
        if not event.start_date or not event.end_date:
            return Response({"error": "start_date and end_date are required for this event type"}, status=400)
        date_list = [event.start_date + timedelta(days=x) for x in range((event.end_date - event.start_date).days + 1)]
    elif event.event_occurrence_type == EventOccurrenceType.LIST_OF_DATES:
        date_list = event.event_dates
    else:
        return Response({"error": "Invalid event occurrence type"}, status=400)

    return Response({"dates": date_list}, status=200)


@api_view(['GET'])
def event_availabilities(request, event_id, date):
    try:
        event = Event.objects.get(id=event_id)
        date_obj = datetime.datetime.strptime(date, '%Y-%m-%d')
    except Event.DoesNotExist:
        return Response({"error": "Event not found"}, status=404)
    except ValueError:
        return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=400)

    if event.event_type == EventType.ONE_ON_ONE:
        if event.event_occurrence_type == EventOccurrenceType.RECURRING:
            if date_obj.date() not in [datetime.datetime.strptime(d, '%Y-%m-%d').date() for d in event.event_dates]:
                return Response({"error": "Date is not in the event's list of dates"}, status=400)
        elif event.event_occurrence_type == EventOccurrenceType.BETWEEN_DATES:
            if not (datetime.datetime.combine(event.start_date, datetime.time.min) <= date_obj <= datetime.datetime.combine(
                    event.end_date, datetime.time.min)):
                return Response({"error": "Date is not within the event's start and end dates."}, status=400)
        elif event.event_occurrence_type == EventOccurrenceType.LIST_OF_DATES:
            if date_obj.date() not in [datetime.datetime.strptime(d, '%Y-%m-%d').date() for d in event.event_dates]:
                return Response({"error": "Date is not in the event's list of dates."}, status=400)
    elif event.event_type == EventType.ONE_OFF:
        event_dates = [d['date'] for d in event.event_dates]
        if date not in event_dates:
            return Response({"error": "Date is not in the event's list of dates."}, status=400)

    user = event.user
    try:
        date_obj = datetime.datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=400)

    selected_slots = []
    if event.event_occurrence_type == EventOccurrenceType.RECURRING:
        for date_str in event.event_dates:
            if date_str == date:
                date_time = datetime.datetime.strptime(f"{date_str} {event.recurring_event_time}", '%Y-%m-%d %H:%M:%S')
                selected_slots.append((date_time, date_time + timedelta(minutes=event.duration)))
    elif event.event_type == EventType.ONE_OFF:
        event_slots = [slot for slot in event.event_dates if slot['date'] == date]
        for time_key in event_slots[0]['time_keys']:
            selected_slots.append((datetime.datetime.strptime(time_key.split("_")[0], '%Y-%m-%dT%H:%M:%S'),
                                   datetime.datetime.strptime(time_key.split("_")[1], '%Y-%m-%dT%H:%M:%S')))

    availabilities = fetch_user_calendar(user, date_obj, event.duration, selected_slots)
    return Response({"availabilities": availabilities}, status=200)




# TOD0: Handle Race condition. Need to add selected datetime stamp to a distributed lock
@api_view(['POST'])
def book_event(request, event_id, date):

    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        return Response({"error": "Event not found"}, status=404)

    user = event.user
    try:
        date_obj = datetime.datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=400)

    if event.event_occurrence_type == EventOccurrenceType.BETWEEN_DATES:
        if not (datetime.datetime.combine(event.start_date, datetime.time.min) <= date_obj <= datetime.datetime.combine(
                event.end_date, datetime.time.min)):
            return Response({"error": "Date is not within the event's start and end dates."}, status=400)
    elif event.event_occurrence_type == EventOccurrenceType.LIST_OF_DATES:
        if date_obj.date() not in [datetime.datetime.strptime(d, '%Y-%m-%d').date() for d in event.event_dates]:
            return Response({"error": "Date is not in the event's list of dates."}, status=400)

    availabilities = fetch_user_calendar(user, date_obj, event.duration)

    start_time_str = request.data.get('start_time')
    end_time_str = request.data.get('end_time')

    date_time_key = start_time_str.split("+")[0] + "_" + end_time_str.split("+")[0]


    if not availabilities or not any(slot['key'] == date_time_key for slot in availabilities):
        return Response({"error": "No availabilities found for this date or the specified time slot."}, status=400)

    lock_key = f"lock:{event_id}:{date_time_key}"
    lock = RedisClientSingleton().get_redis_client().lock(lock_key, timeout=60)  # 60 seconds timeout

    if not lock.acquire(blocking=False):
        return Response({"error": "This slot is already being booked. Please try another slot."}, status=400)

    event_data = {
        'summary': event.name,
        'start_time': request.data.get('start_time'),
        'end_time': request.data.get('end_time'),
        'attendees': [request.data.get('attendee_email')],
        'description': event.description,
        'location': event.location,
    }

    try:
        created_event = create_event(user, event_data)
    except Exception as e:
        return Response({"error": str(e)}, status=500)

    return Response({"event": created_event}, status=201)