from django.urls import path
from . import views

urlpatterns = [
    path('branches/', views.branches, name='branches'),
    path('branches/<int:pk>/update/', views.update_branch, name='update_branch'),
    path('branches/<int:pk>/delete/', views.delete_branch, name='delete_branch'),
    path('branches/add/', views.add_branch, name='add_branch'),
]
