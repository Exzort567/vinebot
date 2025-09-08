from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from core.models import AllowedUser
from .forms import AllowedUserForm

@login_required(login_url='/')
@never_cache
def dashboard(request):
    allowed = AllowedUser.objects.filter(
        email__iexact=request.user.email, is_active=True
    ).first()

    if not allowed or allowed.role != "admin":
        return redirect('denied')

    users = AllowedUser.objects.all()
    form = AllowedUserForm()
    return render(request, 'admin_dashboard/dashboard.html', {"users": users, "form": form})


@login_required(login_url='/')
def add_user(request):
    if request.method == "POST":
        form = AllowedUserForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect('admin_dashboard:dashboard')


@login_required(login_url='/')
def edit_user(request, pk):
    user = get_object_or_404(AllowedUser, pk=pk)
    if request.method == "POST":
        form = AllowedUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
    return redirect('admin_dashboard:dashboard')


@login_required(login_url='/')
def delete_user(request, pk):
    user = get_object_or_404(AllowedUser, pk=pk)
    user.delete()
    return redirect('admin_dashboard:dashboard')
