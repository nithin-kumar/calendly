from django.urls import path
from .views import events, handle_event, calendar_days_for_event, event_availabilities, book_event

urlpatterns = [
    path('events/', events, name='event-create'),
    path('events/<str:id>/', handle_event, name='handle_event'),
    path('events/<str:id>/calendar_days', calendar_days_for_event, name='calendar_days_for_event'),
    path('events/<str:event_id>/availabilities/<str:date>/', event_availabilities, name='event_availabilities'),
    path('events/<str:event_id>/availabilities/<str:date>/book/', book_event, name='book_event'),
]