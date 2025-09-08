from django.urls import path
from . import views

app_name = 'admin_dashboard'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('add/', views.add_user, name='add_user'),
    path('edit/<int:pk>/', views.edit_user, name='edit_user'),
    path('delete/<int:pk>/', views.delete_user, name='delete_user'),
]
