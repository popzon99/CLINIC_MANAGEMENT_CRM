from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.franchise_admins_list, name='franchise-admins-list'),
    path('view/<int:admin_id>/', views.view_franchise_admin, name='view-franchise-admin'),
    path('add/', views.add_franchise_admin, name='add-franchise-admin'),
    path('update/<int:admin_id>/', views.update_franchise_admin, name='update-franchise-admin'),
    path('delete/<int:admin_id>/', views.delete_franchise_admin, name='delete-franchise-admin'),
]





