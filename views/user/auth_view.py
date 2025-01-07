from django.shortcuts import render,redirect
from django.contrib import messages
from authentication.models import *
from django.contrib.auth import login,logout,update_session_auth_hash
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

def Register(request):
    if request.method == "GET":
        return render(request, 'user/login-register.html')

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
        return render(request, 'user/login-register.html')

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
    return redirect('/login/')

def Subscribe(request):
    if request.method == "POST":
        email = request.POST.get('email')
        if UserModel.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Email has already been used!'}, status=400)
        else:
            role = RoleModel.objects.get(name="subscriber")
            user = UserModel.objects.create(
                email=email,
                role=role,
            )
            user.save()
            return JsonResponse({'message': 'Email has been successfully subscribed!'}, status=200)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def UpdateProfile(request):
    if request.method == "POST":
        user = UserModel.objects.get(id = request.user.id)
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.phone = request.POST.get('phone')
        user.address = request.POST.get('address')
        if request.FILES.get('profile'):
            user.profile.delete()
            user.profile = request.FILES.get('profile')
        user.save()

        return JsonResponse({
            'message': 'Profile updated successfully!',
            'username': user.username,
            'email': user.email,
            'phone': str(user.phone),
            'address':user.address
        }, status=200)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def ChangePassword(request):
    if request.method == "POST":
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        # Validate current password
        if not request.user.check_password(current_password):
            return JsonResponse({'error': 'Current password is incorrect.'}, status=400)

        # Validate new password and confirmation match
        if new_password != confirm_password:
            return JsonResponse({'error': 'New password and confirmation do not match.'}, status=400)
        
        if new_password == current_password:
            return JsonResponse({'error': 'New password should not be the same as the current password.'}, status= 400)

        # # Validate password strength (Django's built-in validation)
        # if len(new_password) < 8:
        #     return JsonResponse({'error': 'Password must be at least 8 characters long.'}, status=400)

        # Update password
        request.user.set_password(new_password)
        request.user.save()

        # Keep the user logged in after changing the password
        update_session_auth_hash(request, request.user)

        return JsonResponse({'message': 'Password updated successfully!'}, status=200)

    return JsonResponse({'error': 'Invalid request method.'}, status=400)