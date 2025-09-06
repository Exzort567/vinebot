from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from core.models import AllowedUser
from django.views.decorators.cache import never_cache

@login_required(login_url='/')
@never_cache
def dashboard(request):
    allowed = AllowedUser.objects.filter(
        email__iexact=request.user.email, is_active=True
    ).first()

    if not allowed or allowed.role != "admin":
        return redirect('denied')
    
    users = AllowedUser.objects.all()
    return render(request, 'admin_dashboard/dashboard.html', {"users": users})
