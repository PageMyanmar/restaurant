from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.contrib.auth import login,logout
from authentication.models import *

def AdminLogin(request):
    if request.method == "GET":
        return render(request, 'admin/login.html')
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = UserModel.objects.get(email=email)
            if check_password(password, user.password):
                # Specify the backend explicitly
                login(request, user)
                messages.success(request, f"Welcome {user.username}")
                return redirect('/dashboard/')
            else:
                messages.error(request, "Email or Password is incorrect!")
                return redirect('/khaing/')
        except UserModel.DoesNotExist:
            messages.error(request, "Email or Password is incorrect!")
            return redirect('/khaing/')

def AdminLogout(request):
    logout(request)
    return redirect('/khaing/')