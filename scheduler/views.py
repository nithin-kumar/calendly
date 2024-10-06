import datetime
import os

import google
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.conf import settings
from google_auth_oauthlib.flow import Flow
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from googleapiclient.discovery import build

from scheduler.models import GoogleCredentials
from scheduler.services import fetch_user_calendar

CLIENT_SECRETS_FILE = os.path.join(settings.BASE_DIR, 'client_secret.json')

SCOPES = ['https://www.googleapis.com/auth/calendar', 'openid',
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile']


@api_view(['GET'])
def health_check(request):
    return Response({'status': 'ok'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def google_calendar_init(request):
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri='https://3b9d-103-175-137-13.ngrok-free.app/api/google-calendar/callback',
    )
    authorization_url, state = flow.authorization_url(
        access_type='offline',
    )
    return redirect(authorization_url)

@api_view(['GET'])

def google_calendar_callback(request):
    state = request.GET.get('state')
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        state=state,
        redirect_uri='https://3b9d-103-175-137-13.ngrok-free.app/api/google-calendar/callback'
    )


    flow.fetch_token(authorization_response=request.build_absolute_uri())
    service = build('people', 'v1', credentials=flow.credentials)
    profile = service.people().get(resourceName='people/me', personFields='emailAddresses').execute()
    email = profile.get('emailAddresses')[0].get('value')
    user = User.objects.get(username=email.lower())
    GoogleCredentials.objects.update_or_create(
        user=user,
        defaults={
            'token': flow.credentials.token,
            'token_uri': flow.credentials.token_uri,
            'client_id': flow.credentials.client_id,
            'client_secret': flow.credentials.client_secret,
            'scopes': flow.credentials.scopes,
        }
    )
    return Response({'message': 'Google Calendar linked successfully'})

def credentials_to_dict(credentials):
    return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }


@api_view(['GET'])
def fetch_calendar_events(request):
    credentials = get_credentials_from_session(request)
    if not credentials:
        return Response({'error': 'Credentials not found'}, status=400)

    start_time = datetime.datetime.combine(
        datetime.datetime.strptime(request.GET.get('date', datetime.datetime.today().strftime('%Y-%m-%d')),
                                   '%Y-%m-%d').date(), datetime.datetime.min.time())
    duration = int(request.GET.get('duration')) if request.GET.get('duration') else 30
    try:
        filtered_slots, timezone = fetch_user_calendar(request.user, start_time, duration, [])
    except google.auth.exceptions.RefreshError:
        return Response({"error": "Google credentials expired. Please re-authenticate."}, status=401)
    return Response(filtered_slots)

def get_credentials_from_session(request):
    user = request.user
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

