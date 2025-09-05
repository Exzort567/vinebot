from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from .models import AllowedUser
from django.views.decorators.cache import never_cache

def login_page(request):
    return render(request, 'core/login.html')

@login_required(login_url='/')
@never_cache
def post_login(request):
    email = request.user.email
    try:
        allowed = AllowedUser.objects.get(email__iexact=email, is_active=True)
    except AllowedUser.DoesNotExist:
        auth_logout(request)
        return redirect('denied')

    # Decide where to redirect based on role
    if allowed.role.strip().lower() == "admin":
        return redirect('admin_dashboard:dashboard')

    return redirect('chatbot')

@login_required(login_url='/')
@never_cache
def chatbot_page(request):
    email = request.user.email

    if not AllowedUser.objects.filter(email__iexact=email, is_active=True).exists():
        return redirect('denied')

    return render(request, 'core/chatbot.html')

def access_denied(request):
    return render(request, 'core/access_denied.html')
