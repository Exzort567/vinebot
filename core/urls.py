from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.login_page, name='login'),
    path('post-login/', views.post_login, name='post_login'),
    path('chatbot/', views.chatbot_page, name='chatbot'),
    path('denied/', views.access_denied, name='denied'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),

    # New chat history endpoints
    path("chat/new/", views.new_chat, name="chat_new"),  # ✅ matches your views.py
    path("chat/history/", views.chat_history, name="chat_history"),
    path("chat/<int:chat_id>/messages/", views.get_chat, name="chat_messages"),
    path("chat/<int:chat_id>/rename/", views.rename_chat, name="chat_rename"),
    path("chat/<int:chat_id>/delete/", views.delete_chat, name="chat_delete"),
    path("chat-api/", views.chat_api, name="chat_api"),
]
