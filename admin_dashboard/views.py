from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from core.models import AllowedUser

@login_required
def dashboard(request):
    try:
        allowed = AllowedUser.objects.get(email__iexact=request.user.email, is_active=True)
    except AllowedUser.DoesNotExist:
        return redirect('denied')

    if allowed.role != 'admin':
        return redirect('denied')

    return render(request, 'admin_dashboard/dashboard.html')
