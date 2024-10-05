from events.models import EventBooking


def insert_event_booking(event_id, email):

    event_booking = EventBooking(
        event_id=event_id,
        attendee_email=email
    )
    event_booking.save()
    return event_booking