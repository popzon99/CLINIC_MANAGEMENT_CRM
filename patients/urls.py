from django.urls import path
from . import views  # Importing views from the current directory

# URL patterns for the 'patients' app
urlpatterns = [
    # Adding a new patient; mapped to the 'add_new_patient' view function
    path('add/', views.add_new_patient, name='add_new_patient'),

    # Listing all patients; mapped to the 'patient_list' view function
    path('list/', views.patient_list, name='patient_list'),

    # Displaying a specific patient's profile; 
    # Uses a class-based view 'PatientProfileView' and includes patient_id as a variable in the URL
    path('profile/<int:patient_id>/', views.PatientProfileView.as_view(), name='patient_profile'),

    # Fetching details of a specific patient as JSON; mapped to 'get_patient_details' view function
    # The 'int:patient_id' captures an integer parameter from the URL and passes it to the view
    path('details/<int:patient_id>/', views.get_patient_details, name='get_patient_details'),

    # Updating a specific patient's information; mapped to 'update_patient' view function
    # Includes patient_id as a variable in the URL
    path('update/<int:patient_id>/', views.update_patient, name='update_patient'),

    # Deleting a specific patient; mapped to 'delete_patient' view function
    # Includes patient_id as a variable in the URL
    path('delete/<int:patient_id>/', views.delete_patient, name='delete_patient'),
]
