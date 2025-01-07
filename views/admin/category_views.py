from myadmin.models import CategoryModel
from django.shortcuts import render,redirect
from django.contrib import messages

def Categories(request):
    categories = CategoryModel.objects.all().order_by('-created_at')
    context = {
        'categories':categories
    }
    return render(request, 'user/categories.html',context)

def CreateCategory(request):
    if request.method == "GET":
        return render(request,"user/create-category.html")
    if request.method == "POST":
        category = CategoryModel.objects.create(
            name = request.POST.get('name'),
            image = request.FILES.get('image')
        )
        category.save()
        messages.success(request,"Category is created successfully!")
        return redirect('/categories/')
    
def UpdateCategory(request,id):
    category = CategoryModel.objects.get(id = id)
    if request.method == "GET":
        context = {
            'category':category
        }
        return render(request,"user/update-category.html",context)
    if request.method == "POST":
        category.name = request.POST.get('name')
        if request.FILES.get('image'):
            category.image.delete()
            category.image = request.FILES.get('image')
        category.save()
        messages.success(request,"Category is updated successfully")
        return redirect("/categories/")
    
def DeleteCategory(request,id):
    category = CategoryModel.objects.get(id = id)
    if category.image:
        category.image.delete()
    category.delete()
    messages.success(request,"Category is deleted successfully!")
    return redirect('/categories/')