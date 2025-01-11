from django.shortcuts import render,redirect
from django.contrib import messages
from authentication.models import *
from django.contrib.auth import login,logout
from django.contrib.auth.hashers import check_password
from django.conf import settings

def Register(request):
    if request.method == "GET":
        return render(request, 'login-register.html')

    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get("email")

        if UserModel.objects.filter(email=email).exists():
            messages.error(request,"Email has been already used")
            return redirect(settings.LOGIN_URL)

        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password == confirm_password:
            user = UserModel.objects.create_user(
                username=username,
                email=email,
                password=password,
            )
            user.save()
            login(request, user)
            messages.success(request,f"Account was created for {username}")
            return redirect('/')
        else:
            messages.error(request,"Password and confirm password do not match!")
            return redirect(settings.LOGIN_URL)


def Login(request):
    if request.method == "GET":
        return render(request, 'login-register.html')

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = UserModel.objects.get(email=email)
            if check_password(password, user.password):
                login(request, user)
                messages.success(request,f"Welcome {user.username}")
                return redirect('/')
            else:
                messages.error(request,"Email or Password is incorrect!")
                return redirect(settings.LOGIN_URL)
        
        except UserModel.DoesNotExist:
            messages.error(request,"Email or Password is incorrect!")
            return redirect(settings.LOGIN_URL)

def Logout(request):
    logout(request)
    return redirect('/')