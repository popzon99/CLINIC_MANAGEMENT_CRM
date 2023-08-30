from django.urls import path
from . import views

app_name = 'appointments'  # This is for namespacing your URLs

urlpatterns = [
    # Schedule appointment
    path('schedule/', views.schedule_appointment, name='schedule_appointment'),
    path('schedule/<int:patient_id>/', views.schedule_appointment, name='schedule_appointment_with_patient'),

    # List appointments
    path('list/', views.list_appointments, name='list_appointments'),

    # Delete appointment
    path('delete/<int:appointment_id>/', views.delete_appointment, name='delete_appointment'),

    # Calendar view
    path('calendar/', views.calendar_view, name='calendar_view'),
]
