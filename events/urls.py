from django.urls import path
from .views import events, handle_event, calendar_days_for_event, event_availabilities, book_event, list_user_events, \
    pause_event, activate_event

urlpatterns = [
    path('events/', events, name='event-create'),
    path('events/<str:id>/', handle_event, name='handle_event'),
    path('events/<str:id>/calendar_days', calendar_days_for_event, name='calendar_days_for_event'),
    path('events/<str:event_id>/availabilities/<str:date>/', event_availabilities, name='event_availabilities'),
    path('events/<str:event_id>/availabilities/<str:date>/book/', book_event, name='book_event'),
    path('get_events/', list_user_events, name='list_user_events'),
    path('events/<str:event_id>/pause', pause_event, name='pause_event'),
    path('events/<str:event_id>/unpause', activate_event, name='activate_event'),
]