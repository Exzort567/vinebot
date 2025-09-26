from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from .models import AllowedUser, Chat, Message
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
from django.views.decorators.cache import never_cache
from django.http import JsonResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from .chatbot_model_handler import ModelHandler
import os
from dotenv import load_dotenv
import json

load_dotenv()

SPACE_NAME = os.getenv("SPACE_NAME")
model_handler = ModelHandler(SPACE_NAME)

# Create new chat
@login_required
@csrf_exempt
@require_http_methods(["POST"])
def new_chat(request):
    chat = Chat.objects.create(user=request.user)
    return JsonResponse({"chat_id": chat.id, "title": chat.title})

# Get all chats for the logged in user
@login_required
def chat_history(request):
    chats = Chat.objects.filter(user=request.user).order_by("-created_at")
    return JsonResponse({
        "chats": [
            {"id": chat.id, "title": chat.title or f"Chat {chat.id}"}
            for chat in chats
        ]
    })

# Get message in chat
@login_required
def get_chat(request, chat_id):
    try:
        chat = Chat.objects.get(id=chat_id, user=request.user)
    except Chat.DoesNotExist:
        return JsonResponse({"error": "Chat not found"}, status=404)
    
    messages = chat.messages.order_by("timestamp").values("sender", "content", "timestamp")
    return JsonResponse(list(messages), safe=False)

# Rename chat
@login_required
@csrf_exempt
@require_http_methods(["POST"])
def rename_chat(request, chat_id):
    try:
        chat = Chat.objects.get(id=chat_id, user=request.user)
    except Chat.DoesNotExist:
        return JsonResponse({"error": "Chat not found"}, status=400)

    body = json.loads(request.body.decode("utf-8"))
    new_title = body.get("title")

    if new_title:
        chat.title = new_title
        chat.save()
        return JsonResponse({"success": True, "title": new_title})
    return JsonResponse({"error": "No title provided"}, status=404)

# Delete chat
@login_required
@csrf_exempt
@require_http_methods(["POST", "DELETE"])
def delete_chat(request, chat_id):
    try:
        chat = Chat.objects.get(id=chat_id, user=request.user)
        chat.delete()
        return JsonResponse({"Success": True})
    except Chat.DoesNotExist:
        return JsonResponse({"error": "Chat not found"}, status=404)
    


@csrf_exempt
@login_required
def chat_api_stream(request):
    if request.method == "POST":
        body = json.loads(request.body.decode("utf-8"))
        user_message = body.get("message", "")
        chat_id = body.get("chat_id")

        if not user_message or not chat_id:
            return JsonResponse({"error": "Message and chat_id is required"}, status=400)

        try:
            chat = Chat.objects.get(id=chat_id, user=request.user)
        except Chat.DoesNotExist:
            return JsonResponse({"error": "Chat not found"}, status=404)

        # Save user message
        Message.objects.create(chat=chat, sender="user", content=user_message)

        if chat.title == "New Chat":
            title = user_message[:25] + ("..." if len(user_message) > 25 else "")
            chat.title = title
            chat.save()

        def event_stream():
            try:
                for chunk in model_handler.stream_response(user_message):
                    yield f"data: {chunk}\n\n"
            except Exception as e:
                yield f"data: Error: {str(e)}\n\n"

        response = StreamingHttpResponse(event_stream(), content_type="text/event-stream")
        response["Cache-Control"] = "no-cache"
        return response

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
