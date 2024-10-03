from django.urls import path
from .views import google_calendar_callback, google_calendar_init, fetch_calendar_events

urlpatterns = [
    path('google-calendar/init/', google_calendar_init, name='google-calendar-init'),
    path('google-calendar/callback/', google_calendar_callback, name='google-calendar-callback'),
    path('availabilities/', fetch_calendar_events, name='availabilities'),
]