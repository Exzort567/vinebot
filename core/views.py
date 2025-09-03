from django.shortcuts import render

def login_page(request):
    return render(request, 'core/login.html')

def chatbot_page(request):
    return render(request, 'core/chatbot.html')

def admin_dashboard(request):
    return render(request, 'core/dashboard.html')

def access_denied(request):
    return render(request, 'core/access_denied.html')
