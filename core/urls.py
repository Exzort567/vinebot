from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.login_page, name='login'),
    path('post-login/', views.post_login, name='post_login'),
    path("chat-api/", views.chat_api, name="chat_api"),
    path('chatbot/', views.chatbot_page, name='chatbot'),
    path('denied/', views.access_denied, name='denied'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
]
