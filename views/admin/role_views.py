from django.shortcuts import render,redirect
from authentication.models import *
from django.contrib.auth.models import Permission
from django.contrib import messages

def Roles(request):
    roles = RoleModel.objects.all().order_by('-created_at')
    permissions = Permission.objects.all()
    context = {
        'roles': roles,
        'permissions': permissions
    }
    return render(request,'admin/roles.html',context)

def RoleCreate(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        
        if RoleModel.objects.filter(name=name).exists():
            messages.error(request, "Role Name has already been used!")
            return redirect('/roles/')
        
        selected_permissions = request.POST.getlist('permissions')
        if not selected_permissions:
            messages.warning(request, "Please select at least one permission.")
            return redirect('/roles/')
        
        role = RoleModel.objects.create(name=name)
        role.permissions.set(selected_permissions)
        role.save()
        
        messages.success(request, "Role created successfully.")
        return redirect('/roles/')  

def RoleUpdate(request, id):
    role = RoleModel.objects.get(id = id)
    if request.method == 'POST':
        new = request.POST.get('name')
        selected_permissions = request.POST.getlist('permissions')

        current_permissions = set(role.permissions.values_list('id', flat=True))
        new_permissions = set(map(int, selected_permissions))

        if role.name == new and current_permissions == new_permissions:
            messages.warning(request, 'No changes were made.')
            return redirect('/roles/')

        role.name = new
        role.permissions.set(new_permissions)
        role.save()

        messages.success(request, 'Role updated successfully.')
        return redirect('/roles/')

def RoleDelete(request, id):
    role = RoleModel.objects.get(id = id)
    role.delete()
    messages.success(request, "Role deleted successfully.")
    return redirect('/roles/')