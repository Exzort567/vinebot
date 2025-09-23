from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from .models import AllowedUser
from django.views.decorators.cache import never_cache
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .chatbot_model_handler import ModelHandler
import os
from dotenv import load_dotenv
import json

load_dotenv()

SPACE_NAME = os.getenv("SPACE_NAME")
model_handler = ModelHandler(SPACE_NAME)


@csrf_exempt
def chat_api(request):
    if request.method == "POST":
        body = json.loads(request.body.decode("utf-8"))
        user_message = body.get("message", "")
        if not user_message:
            return JsonResponse({"error": "Message is required"}, status=400)

        bot_reply = model_handler.generate_response(user_message)
        return JsonResponse({"reply": bot_reply})
    return JsonResponse({"error": "Invalid request method"}, status=405)

def login_page(request):
    return render(request, 'core/login.html')

@login_required(login_url='/')
@never_cache
def post_login(request):
    email = request.user.email
    print(f"[DEBUG] post_login called for {email}")

    try:
        allowed = AllowedUser.objects.get(email__iexact=email, is_active=True)
        print(f"[DEBUG] AllowedUser found: {allowed.email}, role={allowed.role}")
    except AllowedUser.DoesNotExist:
        print(f"[DEBUG] No AllowedUser found for {email}, logging out...")
        auth_logout(request)
        return redirect('denied')

    if allowed.role.strip().lower() == "admin":
        print("[DEBUG] Redirecting to admin dashboard")
        return redirect('admin_dashboard:dashboard')

    print("[DEBUG] Redirecting to chatbot")
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
