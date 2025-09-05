from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from core.models import AllowedUser
from django.views.decorators.cache import never_cache

@login_required(login_url='/')
@never_cache
def dashboard(request):
    try:
        allowed = AllowedUser.objects.get(email__iexact=request.user.email, is_active=True)
    except AllowedUser.DoesNotExist:
        return redirect('denied')

    if allowed.role != 'admin':
        return redirect('denied')

    return render(request, 'admin_dashboard/dashboard.html')
