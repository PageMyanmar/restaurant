from django.http import JsonResponse
from django.shortcuts import redirect,render
from myadmin.models import *
from user.models import *
import json
from django.contrib import messages

# View to render the main page with a table list
def Tables(request):
    tables = TableModel.objects.all()
    context = {
        'tables':tables
    }
    return render(request, 'user/tables.html', context)
    
def CreateTable(request):
    if request.method == "GET":
        return render(request,"user/create-table.html")
    if request.method == "POST":
        table = TableModel.objects.create(
            name = request.POST.get('name')
        )
        table.save()
        messages.success(request,"Table is created successfully!")
        return redirect('/tables/')

def UpdateTable(request,id):
    table = TableModel.objects.get(id = id)
    if request.method == "GET":
        context = {
            'table':table
        }
        return render(request,"user/update-table.html",context)
    if request.method == "POST":
        table.name = request.POST.get('name')
        table.save()
        messages.success(request,"Table is updated successfully!")
        return redirect('/tables/')

def DeleteTable(request,id):
    table = TableModel.objects.get(id = id)
    table.delete()
    messages.success(request,"Table is deleted successfully!")
    return redirect('/tables/')
    
def Order(request, id):
    table = TableModel.objects.get(id=id)
    products = ProductModel.objects.all().order_by('-created_at')
    categories = CategoryModel.objects.all().order_by('-created_at')
    context = {
        "table": table,
        "products": products,
        "categories": categories
    }
    return render(request, 'user/order.html',context)