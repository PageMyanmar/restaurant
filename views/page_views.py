from django.shortcuts import render,redirect
from app.models import *
from collections import defaultdict
from django.contrib import messages

def Index(request):
    categories = CategoryModel.objects.all().order_by('-created_at')
    products = ProductModel.objects.all().order_by("-created_at")
    
    context = {
        'categories': categories,
        'products': products,
    }
    return render(request, 'index.html',context)

def ProductsByCategory(request,id,t_id):
    category = CategoryModel.objects.get(id = id)
    table = TableModel.objects.get(id = t_id)
    products = ProductModel.objects.filter(category = category).order_by("-created_at")
    
    context = {
        'products': products,
        'category': category,
        'table': table,
    }
    return render(request, 'products-by-category.html',context)

def Products(request):
    products = ProductModel.objects.all().order_by("-created_at") 

    context = {
        'products': products
        }
    return render(request, 'shop.html',context)

def Contact(request):
    if request.method == "GET":
        return render(request, 'contact.html')
    if request.method == 'POST':
        contact = ContactModel.objects.create(
            name=request.POST.get('name'),
            phone = request.POST.get('phone'),
            subject = request.POST.get('subject'),
            message = request.POST.get('message')
        )
        contact.save()
        messages.success(request, 'Your message has been sent successfully!')
        return redirect('/contact/')

def Invoices(request):
    invoices = CheckoutModel.objects.all().order_by('-created_at')
    grouped_invoices = []

    for invoice in invoices:
        grouped_items = defaultdict(lambda: {'quantity': 0, 'total_price': 0, 'product': None})

        # Group products by name and sum their quantities and prices
        for cart in invoice.cart_items.all():
            grouped_items[cart.product.id]['quantity'] += cart.quantity
            grouped_items[cart.product.id]['total_price'] += cart.total_price
            grouped_items[cart.product.id]['product'] = cart.product
        
        # Prepare the final list of grouped items for rendering
        grouped_invoices.append({
            'invoice': invoice,
            'items': grouped_items.values()
        })

    context = {
        'grouped_invoices': grouped_invoices,
    }
    return render(request, 'invoices.html', context)
