from django.shortcuts import render,redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from myadmin.decorators import role_permission_required
from myadmin.models import *
from django.contrib import messages

# @login_required(login_url=settings.LOGIN_URL)
# @role_permission_required('account.add_usermodel')
def UserCreate(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get("email")
        is_active = request.POST.get('is_active') == 'on'
        is_staff = request.POST.get('is_staff') == 'on'
        is_superuser = request.POST.get('is_superuser') == 'on'
        role_id = request.POST.get('role')
        
        if UserModel.objects.filter(email=email).exists():
            messages.error(request, "Email has already been used!")
            return redirect('/users/')
        
        password = request.POST.get('password')
        password_confirm = request.POST.get('passwordconfirm')
        if password == password_confirm:
            user = UserModel.objects.create_user(
                username=username,
                email=email,
                password=password,
                is_active=is_active,
                is_staff=is_staff,
                role_id=role_id
            )
            user.save()
            messages.success(request, "Account was created for " + username)
            return redirect('/users/')
        else:
            messages.error(request, "Password does not match! Please check your password again!")
            return redirect('/users/')

# @login_required(login_url=settings.LOGIN_URL)
# @role_permission_required('account.view_usermodel')
def Users(request):
    users = UserModel.objects.all().order_by('-created_at')
    roles = RoleModel.objects.all().order_by('-created_at')
    context = {
        "users": users,
        "roles": roles
    }
    return render(request, 'admin/users.html',context)

# @login_required(login_url=settings.LOGIN_URL)
# @role_permission_required('account.change_usermodel')
def UserUpdate(request, id):
    user = UserModel.objects.get(id=id)
    if request.method == 'POST':
        user.email = request.POST.get('email')
        user.username = request.POST.get('username')
        user.is_active = request.POST.get('is_active') == 'on'
        user.is_staff = request.POST.get('is_staff') == 'on'
        user.is_superuser = request.POST.get('is_superuser') == 'on'
        user.role_id = request.POST.get('role')
        if request.POST.get('password'):
            user.set_password(request.POST.get('password'))
        user.save()
        return redirect('/users/')

# @login_required(login_url=settings.LOGIN_URL)
# @role_permission_required('account.delete_usermodel')
def UserDelete(request, id):
    user = UserModel.objects.get(id=id)
    user.delete()
    return redirect('/users/')