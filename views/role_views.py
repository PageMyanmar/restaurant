from django.shortcuts import render,redirect
from authentication.models import *
from django.contrib.auth.models import Permission
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required
from app.decorators import role_permission_required

@login_required(login_url=settings.LOGIN_URL)
@role_permission_required('app.view_rolemodel')
def Roles(request):
    roles = RoleModel.objects.all().order_by('-created_at')
    context = {
        'roles': roles
    }
    return render(request,'roles.html',context)

@login_required(login_url=settings.LOGIN_URL)
@role_permission_required('app.add_rolemodel')
def CreateRole(request):
    if request.method == "GET":
        permissions = Permission.objects.all()
        context ={
            'permissions': permissions
        }
        return render(request,"create-role.html",context)
    if request.method == 'POST':
        name = request.POST.get('name')
        
        if RoleModel.objects.filter(name=name).exists():
            messages.error(request, "Role Name has already been used!")
            return redirect('/create-role/')
        
        selected_permissions = request.POST.getlist('permissions')
        if not selected_permissions:
            messages.warning(request, "Please select at least one permission.")
            return redirect('/create-role/')
        
        role = RoleModel.objects.create(name=name)
        role.permissions.set(selected_permissions)
        role.save()
        
        messages.success(request, "Role created successfully.")
        return redirect('/roles/')  

@login_required(login_url=settings.LOGIN_URL)
@role_permission_required('app.change_rolemodel')
def UpdateRole(request, id):
    role = RoleModel.objects.get(id = id)
    if request.method == "GET":
        permissions = Permission.objects.all()
        context ={
            'role': role,
            'permissions': permissions
        }
        return render(request,"update-role.html",context)
    if request.method == 'POST':
        new = request.POST.get('name')
        selected_permissions = request.POST.getlist('permissions')

        current_permissions = set(role.permissions.values_list('id', flat=True))
        new_permissions = set(map(int, selected_permissions))

        if role.name == new and current_permissions == new_permissions:
            messages.warning(request, 'No changes were made.')
            return redirect(f'/update-role/{role.id}/')

        role.name = new
        role.permissions.set(new_permissions)
        role.save()

        messages.success(request, 'Role updated successfully.')
        return redirect('/roles/')

@login_required(login_url=settings.LOGIN_URL)
@role_permission_required('app.delete_rolemodel')
def DeleteRole(request, id):
    role = RoleModel.objects.get(id = id)
    role.delete()
    messages.success(request, "Role deleted successfully.")
    return redirect('/roles/')