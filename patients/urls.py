from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_new_patient, name='add_patient'),
    path('', views.patient_list, name='patient_list'),
    path('profile/<int:patient_id>/', views.patient_profile, name='patient_profile'),
    path('update/<int:patient_id>/', views.update_patient, name='update_patient'),
    path('delete/<int:patient_id>/', views.delete_patient, name='delete_patient'),
]
