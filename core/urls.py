from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_page, name='login'),
    path('chatbot/', views.chatbot_page, name='chatbot'),
    path('dashboard/', views.admin_dashboard, name='dashboard'),
    path('denied/', views.access_denied, name='denied'),
    path('logout/', views.admin_dashboard, name='logout'),
]
