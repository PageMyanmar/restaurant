from django.shortcuts import redirect,render
from app.models import *
from app.models import *
from django.contrib import messages
from django.db import transaction
from collections import defaultdict

# View to render the main page with a table list
def Tables(request):
    tables = TableModel.objects.all()
    context = {
        'tables':tables
    }
    return render(request, 'tables.html', context)
    
def CreateTable(request):
    if request.method == "GET":
        return render(request,"create-table.html")
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
        return render(request,"update-table.html",context)
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
    return render(request, 'order.html',context)

@transaction.atomic
def Checkout(request, id):
    # Get the table object by its ID
    table = TableModel.objects.get(id=id)
    
    # Filter the active cart items for the specific table
    cart_items = CartModel.objects.filter(table=table, status=True)

    # Group cart items by product and calculate combined quantities and subtotals
    grouped_cart = defaultdict(lambda: {"quantity": 0, "total_price": 0, "product": None})
    for cart in cart_items:
        product_id = cart.product.id
        grouped_cart[product_id]["product"] = cart.product
        grouped_cart[product_id]["quantity"] += cart.quantity
        grouped_cart[product_id]["total_price"] += cart.total_price

    grouped_cart_items = list(grouped_cart.values())
    
    # Calculate the subtotal for the grouped cart items
    total = sum(item["total_price"] for item in grouped_cart_items)

    if request.method == "POST":
        # Create a new CheckoutModel instance and save it
        checkout = CheckoutModel.objects.create(
            payment_id=request.POST.get('payment'),
            total=total,
            table=table,
        )
        checkout.cart_items.set(cart_items)
        checkout.save()

        CartModel.objects.filter(table=table).update(table=None)
        table.status = False
        table.save()

        return redirect('/tables/')
    else:
        # Prepare the context for GET request
        payments = PaymentModel.objects.all().order_by('-created_at')
        context = {
            'table': table,
            'cart_items': grouped_cart_items,
            'total': total,
            'payments': payments
        }
        return render(request, "checkout.html", context)