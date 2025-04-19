from django.urls import path
from . import views

app_name = 'BookMeeting'

urlpatterns = [
    path('bookmeeting/',views.book_meeting, name='bookmeeting'),
    path('fetch-events/',views.fetch_events, name='fetch_events'),
]
