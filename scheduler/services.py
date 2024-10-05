import datetime

import google
import pytz
from googleapiclient.discovery import build
from scheduler.models import GoogleCredentials


def fetch_user_calendar(user, start_time, duration, generated_slots = []):

    credentials = get_credentials_from_user(user)
    if not credentials:
        raise Exception('Credentials not found')


    end_time = start_time + datetime.timedelta(days=1)
    if not generated_slots:
        current_time = start_time
        while current_time < end_time:
            slot_end_time = current_time + datetime.timedelta(minutes=duration)
            if current_time.strftime('%Y-%m-%d %H:%M:%S') >= datetime.datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S'):
                generated_slots.append((current_time, slot_end_time))
            current_time = slot_end_time

    service = build('calendar', 'v3', credentials=credentials)
    events_result = service.events().list(calendarId='primary', maxResults=10, singleEvents=True,
                                          orderBy='startTime',
                                          timeMin=datetime.datetime.combine(start_time.date(),
                                                                            datetime.time.min).isoformat() + 'Z',
                                          timeMax=datetime.datetime.combine(start_time.date(),
                                                                            datetime.time.max).isoformat() + 'Z'
                                          ).execute()
    events = events_result.get('items', [])
    filtered_slots = []
    for slot_start, slot_end in generated_slots:
        slot_start = pytz.timezone(events_result["timeZone"]).localize(slot_start)
        formatted_start = slot_start.strftime('%Y-%m-%dT%H:%M:%S%z')
        formatted_start = formatted_start[:-2] + ':' + formatted_start[-2:]

        slot_end = pytz.timezone(events_result["timeZone"]).localize(slot_end)
        formatted_end = slot_end.strftime('%Y-%m-%dT%H:%M:%S%z')
        formatted_end = formatted_end[:-2] + ':' + formatted_end[-2:]

        slot_overlap = False
        for event in events:
            event_start = datetime.datetime.fromisoformat(event['start']['dateTime'])
            event_end = datetime.datetime.fromisoformat(event['end']['dateTime'])
            if slot_start < event_end and event_start < slot_end:
                slot_overlap = True
                break
        if not slot_overlap:
            filtered_slots.append(
                {'start': formatted_start, 'end': formatted_end,
                 'key': f"{slot_start.strftime('%Y-%m-%dT%H:%M:%S')}_{slot_end.strftime('%Y-%m-%dT%H:%M:%S')}"})


    return filtered_slots, events_result["timeZone"]



def create_event(user, event_data):
    credentials = get_credentials_from_user(user)
    if not credentials:
        raise Exception('Credentials not found')

    service = build('calendar', 'v3', credentials=credentials)

    event = {
        'summary': event_data['summary'],
        'location': event_data.get('location', ''),
        'description': event_data.get('description', ''),
        'start': {
            'dateTime': event_data['start_time'],
            'timeZone': event_data['timezone'],
        },
        'end': {
            'dateTime': event_data['end_time'],
            'timeZone': event_data['timezone'],
        },
        'attendees': [{'email': attendee, 'responseStatus': 'accepted'} for attendee in event_data.get('attendees', [])],
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    return event



def get_credentials_from_user(user):
    try:
        google_credentials = GoogleCredentials.objects.get(user=user)
    except GoogleCredentials.DoesNotExist:
        return None

    return google.oauth2.credentials.Credentials(
        token=google_credentials.token,
        refresh_token=google_credentials.refresh_token,
        token_uri=google_credentials.token_uri,
        client_id=google_credentials.client_id,
        client_secret=google_credentials.client_secret,
        scopes=google_credentials.scopes
    )


