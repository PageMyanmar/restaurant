from django.shortcuts import render,redirect
from django.contrib import messages
from myadmin.models import ProductModel, CategoryModel

# View to display all products
def Products(request):
    products = ProductModel.objects.select_related('category').all()
    categories = CategoryModel.objects.all()
    context = {
        'products': products,
        'categories': categories
    }
    return render(request, 'user/products.html', context)

# Create Product
def CreateProduct(request):
    categories = CategoryModel.objects.all().order_by('-created_at')
    if request.method == "GET":
        context = {
            'categories':categories
        }
        return render(request,"user/create-product.html",context)
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
    
def UpdateProduct(request,id):
    categories = CategoryModel.objects.all().order_by('-created_at')
    product = ProductModel.objects.get(id = id)
    if request.method == "GET":
        context = {
            'categories':categories,
            'product':product
        }
        return render(request,"user/update-product.html",context)
    
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
    
def DeleteProduct(request,id):
    product = ProductModel.objects.get(id = id)
    if product.image:
        product.image.delete()
    product.delete()
    messages.success(request,"Product is deleted successfully!")
    return redirect('/products/')