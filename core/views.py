from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from .models import AllowedUser


def login_page(request):
    return render(request, 'core/login.html')


@login_required
def post_login(request):
    email = request.user.email
    print("DEBUG: Logged in email =", email)  # 🔍 check which email logged in

    try:
        allowed = AllowedUser.objects.get(email__iexact=email, is_active=True)
        print(f"DEBUG: Allowed user found: {allowed.email}, role={allowed.role}")
    except AllowedUser.DoesNotExist:
        print("DEBUG: User not in AllowedUser table, logging out...")
        auth_logout(request)
        return redirect('denied')

    # Decide where to redirect based on role
    if allowed.role.strip().lower() == "admin":  # strip in case of spaces
        print("DEBUG: Redirecting → ADMIN dashboard")
        return redirect('admin_dashboard:dashboard')

    print("DEBUG: Redirecting → CHATBOT")
    return redirect('chatbot')


@login_required
def chatbot_page(request):
    email = request.user.email
    print("DEBUG: Accessing chatbot, email =", email)

    if not AllowedUser.objects.filter(email__iexact=email, is_active=True).exists():
        print("DEBUG: User not active in AllowedUser → denied")
        return redirect('denied')

    return render(request, 'core/chatbot.html')


def access_denied(request):
    return render(request, 'core/access_denied.html')
