from django.shortcuts import render,redirect
from django.contrib import messages
from app.models import ProductModel, CategoryModel
from django.conf import settings
from django.contrib.auth.decorators import login_required
from app.decorators import role_permission_required

# View to display all products
@login_required(login_url=settings.LOGIN_URL)
@role_permission_required('app.view_productmodel')
def Products(request):
    products = ProductModel.objects.all().order_by('-created_at')
    context = {
        'products': products
    }
    return render(request, 'products.html', context)

# Create Product
@login_required(login_url=settings.LOGIN_URL)
@role_permission_required('app.add_productmodel')
def CreateProduct(request):
    categories = CategoryModel.objects.all().order_by('-created_at')
    if request.method == "GET":
        context = {
            'categories':categories
        }
        return render(request,"create-product.html",context)
    if request.method == "POST":
        product = ProductModel.objects.create(
            name = request.POST.get('name'),
            price = request.POST.get("price"),
            category_id = request.POST.get('category'),
            image = request.FILES.get('image'),
            quantity = request.POST.get('quantity')
        )
        product.save()
        messages.success(request,"Product is created successfully!")
        return redirect('/products/')
    
@login_required(login_url=settings.LOGIN_URL)
@role_permission_required('app.change_productmodel')
def UpdateProduct(request,id):
    categories = CategoryModel.objects.all().order_by('-created_at')
    product = ProductModel.objects.get(id = id)
    if request.method == "GET":
        context = {
            'categories':categories,
            'product':product
        }
        return render(request,"update-product.html",context)
    
    if request.method == "POST":
        product.name = request.POST.get('name')
        product.price = request.POST.get('price')
        if request.FILES.get('image'):
            product.image.delete()
            product.image = request.FILES.get('image')
        product.category_id = request.POST.get('category')
        product.quantity = request.POST.get('quantity')
        product.save()
        messages.success(request,"Product is updated successfully")
        return redirect('/products/')
    
@login_required(login_url=settings.LOGIN_URL)
@role_permission_required('app.delete_productmodel')
def DeleteProduct(request,id):
    product = ProductModel.objects.get(id = id)
    if product.image:
        product.image.delete()
    product.delete()
    messages.success(request,"Product is deleted successfully!")
    return redirect('/products/')