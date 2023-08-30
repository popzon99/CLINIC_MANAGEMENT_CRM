from django.urls import path
from . import views  # Importing views from the current directory

urlpatterns = [
    # URL mapping for adding a new therapist. Calls 'add_new_therapist' view from 'views.py'.
    path('add/', views.add_new_therapist, name='add_new_therapist'),

    # URL mapping for listing therapists. Calls 'list_therapists' view from 'views.py'.
    path('list/', views.list_therapists, name='list_therapists'),

    # URL mapping for retrieving therapist profile by ID. Calls 'get_therapist_profile' view from 'views.py'.
    path('profile/<int:therapist_id>/', views.get_therapist_profile, name='get_therapist_profile'),

    # URL mapping for adding a new speciality. Calls 'add_new_speciality' view from 'views.py'.
    path('speciality/add/', views.add_new_speciality, name='add_new_speciality'),

    # URL mapping for adding a prescription to an appointment. Calls 'add_prescription' view from 'views.py'.
    path('prescription/add/<int:appointment_id>/', views.add_prescription, name='add_prescription'),

    # URL mapping for getting details of a specific appointment by ID. Calls 'get_appointment_detail' view from 'views.py'.
    path('appointment/<int:appointment_id>/', views.get_appointment_detail, name='get_appointment_detail'),
]
