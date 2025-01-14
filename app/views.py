from django.shortcuts import render,redirect
from django.contrib import messages
from authentication.models import *
from django.contrib.auth import login,logout
from django.contrib.auth.hashers import check_password
from django.conf import settings
from django.db import transaction
from app.models import *
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from collections import defaultdict
from django.contrib.auth.decorators import login_required
from app.decorators import role_permission_required
from django.contrib.auth.models import Permission

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

def Carts(request, id):
    table = TableModel.objects.filter(id=id).first()
    cart_items = CartModel.objects.filter(table=table).order_by('-created_at')
    all_ordered = cart_items.exists() and all(item.status for item in cart_items)
    cart_count = 0
    if table:
        cart_count = CartModel.objects.filter(table=table).count()
    
    for item in cart_items:
        item.total_price = item.quantity * item.product.price
        item.save()
    
    all_total = 0
    for item in cart_items:
        all_total += item.product.price * item.quantity
    
    context = {
        'table_id': table.id if table else None,
        "carts": cart_items,
        "cart_count": cart_count,
        "all_total": all_total,
        "all_ordered": all_ordered
    }
    return render(request, 'carts.html',context)

def AddToCart(request, p_id, t_id):
    if request.method == 'POST':
        table = TableModel.objects.get(id=t_id)
        product = ProductModel.objects.get(id=p_id)
        quantity = int(request.POST.get('quantity', 1))

        # Get the selected size, meat, and spicy from the POST request
        size_id = request.POST.get('size')
        meat_id = request.POST.get('meat')
        spicy_id = request.POST.get('spicy')

        size = SizeModel.objects.get(id=size_id) if size_id else None
        meat = MeatModel.objects.get(id=meat_id) if meat_id else None
        spicy = SpicyModel.objects.get(id=spicy_id) if spicy_id else None

        table.status = True
        table.save()
        product.save()

        # Create the cart entry with the selected size, meat, and spicy
        cart = CartModel.objects.create(
            table=table,
            product=product,
            quantity=quantity,
            note=request.POST.get('note'),
            size=size,
            meat=meat,
            spicy=spicy,
            total_price=product.price * quantity,
            takeaway = request.POST.get('takeaway') == 'on'
        )
        cart.save()

        messages.success(request, f'({cart.quantity}) {cart.product.name} are added to cart successfully! {cart.note}')
        return redirect(f"/order/{table.id}/")
 
def UpdateCart(request, id):
    # Get the cart item to be updated
    cart = CartModel.objects.get(id=id)
    
    if request.method == 'POST':
        # Get the updated quantity and note from the form
        quantity = int(request.POST.get('quantity'))
        note = request.POST.get('note')

        # Get the selected size, meat, and spicy from the POST request
        size_id = request.POST.get('size')
        meat_id = request.POST.get('meat')
        spicy_id = request.POST.get('spicy')

        # Retrieve the selected size, meat, and spicy, or keep the current value if not provided
        size = SizeModel.objects.get(id=size_id) if size_id else cart.size
        meat = MeatModel.objects.get(id=meat_id) if meat_id else cart.meat
        spicy = SpicyModel.objects.get(id=spicy_id) if spicy_id else cart.spicy

        # Update the cart with the new values
        cart.quantity = quantity
        cart.note = note
        cart.size = size
        cart.meat = meat
        cart.spicy = spicy
        cart.total_price = cart.product.price * quantity  # Recalculate total price based on quantity
        cart.takeaway = request.POST.get('takeaway') == 'on'
        cart.save()

        # Show a success message and redirect the user back to the cart page
        messages.success(request, f'Cart updated successfully!')
        return redirect(f"/carts/{cart.table.id}/")  # Redirect to the order page for the specific table

def RemoveFromCart(request,id):
    cart = CartModel.objects.get(id=id)
    product = cart.product
    product.save()
    table = cart.table
    cart.delete()
    messages.success(request, f'{cart.product.name} is removed from cart successfully!')
    return redirect(f'/carts/{table.id}/')

@login_required(login_url=settings.LOGIN_URL)
@role_permission_required('app.view_categorymodel')
def Categories(request):
    categories = CategoryModel.objects.all().order_by('-created_at')
    context = {
        'categories':categories
    }
    return render(request, 'categories.html',context)

@login_required(login_url=settings.LOGIN_URL)
@role_permission_required('app.add_categorymodel')
def CreateCategory(request):
    if request.method == "GET":
        return render(request,"create-category.html")
    if request.method == "POST":
        category = CategoryModel.objects.create(
            name = request.POST.get('name')
        )
        category.save()
        messages.success(request,"Category is created successfully!")
        return redirect('/categories/')
    
@login_required(login_url=settings.LOGIN_URL)
@role_permission_required('app.change_categorymodel')
def UpdateCategory(request,id):
    category = CategoryModel.objects.get(id = id)
    if request.method == "GET":
        context = {
            'category':category
        }
        return render(request,"update-category.html",context)
    if request.method == "POST":
        category.name = request.POST.get('name')
        category.save()
        messages.success(request,"Category is updated successfully")
        return redirect("/categories/")
    
@login_required(login_url=settings.LOGIN_URL)
@role_permission_required('app.delete_categorymodel')
def DeleteCategory(request,id):
    category = CategoryModel.objects.get(id = id)
    category.delete()
    messages.success(request,"Category is deleted successfully!")
    return redirect('/categories/')

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

# View to render the main page with a payment list
@login_required(login_url=settings.LOGIN_URL)
@role_permission_required('app.view_paymentmodel')
def Payments(request):
    payments = PaymentModel.objects.all()
    context = {
        'payments':payments
    }
    return render(request, 'payments.html', context)
    
@login_required(login_url=settings.LOGIN_URL)
@role_permission_required('app.add_paymentmodel')
def CreatePayment(request):
    if request.method == "GET":
        return render(request,"create-payment.html")
    if request.method == "POST":
        payment = PaymentModel.objects.create(
            name = request.POST.get('name'),
            number = request.POST.get('number')
        )
        payment.save()
        messages.success(request,"payment is created successfully!")
        return redirect('/payments/')

@login_required(login_url=settings.LOGIN_URL)
@role_permission_required('app.change_paymentmodel')
def UpdatePayment(request,id):
    payment = PaymentModel.objects.get(id = id)
    if request.method == "GET":
        context = {
            'payment':payment
        }
        return render(request,"update-payment.html",context)
    if request.method == "POST":
        payment.name = request.POST.get('name')
        payment.number = request.POST.get('number')
        payment.save()
        messages.success(request,"payment is updated successfully!")
        return redirect('/payments/')

@login_required(login_url=settings.LOGIN_URL)
@role_permission_required('app.delete_paymentmodel')
def DeletePayment(request,id):
    payment = PaymentModel.objects.get(id = id)
    payment.delete()
    messages.success(request,"payment is deleted successfully!")
    return redirect('/payments/')
    
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
    sizes = SizeModel.objects.all().order_by('-created_at')
    spicies = SpicyModel.objects.all().order_by('-created_at')
    meats = MeatModel.objects.all().order_by('-created_at')
    if request.method == "GET":
        context = {
            'categories':categories,
            'sizes':sizes,
            'spicies':spicies,
            'meats':meats
        }
        return render(request,"create-product.html",context)
    if request.method == "POST":
        product = ProductModel.objects.create(
            name = request.POST.get('name'),
            price = request.POST.get("price"),
            category_id = request.POST.get('category'),
            image = request.FILES.get('image'),
            stock = request.POST.get('stock') == 'on'
        )
        product.save()
        product.size.set(request.POST.getlist('size'))
        product.spicy.set(request.POST.getlist('spicy'))
        product.meat.set(request.POST.getlist('meat'))
        messages.success(request,"Product is created successfully!")
        return redirect('/products/')
    
@login_required(login_url=settings.LOGIN_URL)
@role_permission_required('app.change_productmodel')
def UpdateProduct(request,id):
    categories = CategoryModel.objects.all().order_by('-created_at')
    sizes = SizeModel.objects.all().order_by('-created_at')
    spicies = SpicyModel.objects.all().order_by('-created_at')
    meats = MeatModel.objects.all().order_by('-created_at')
    product = ProductModel.objects.get(id = id)
    if request.method == "GET":
        context = {
            'categories':categories,
            'product':product,
            'sizes':sizes,
            'spicies':spicies,
            'meats':meats
        }
        return render(request,"update-product.html",context)
    
    if request.method == "POST":
        product.name = request.POST.get('name')
        product.price = request.POST.get('price')
        if request.FILES.get('image'):
            product.image.delete()
            product.image = request.FILES.get('image')
        product.category_id = request.POST.get('category')
        product.stock = request.POST.get('stock') == 'on'
        product.save()
        product.size.set(request.POST.getlist('size'))
        product.spicy.set(request.POST.getlist('spicy'))
        product.meat.set(request.POST.getlist('meat'))
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

@login_required(login_url=settings.LOGIN_URL)
@role_permission_required('app.view_tablemodel')
def Tables(request):
    tables = TableModel.objects.all()
    context = {
        'tables':tables
    }
    return render(request, 'tables.html', context)
    
@login_required(login_url=settings.LOGIN_URL)
@role_permission_required('app.add_tablemodel')
def CreateTable(request):
    if request.method == "GET":
        return render(request,"create-table.html")
    if request.method == "POST":
        table = TableModel.objects.create(
            name = request.POST.get('name'),
            status = request.POST.get("status") == 'on'
        )
        table.save()
        messages.success(request,"Table is created successfully!")
        return redirect('/tables/')

@login_required(login_url=settings.LOGIN_URL)
@role_permission_required('app.change_tablemodel')
def UpdateTable(request,id):
    table = TableModel.objects.get(id = id)
    if request.method == "GET":
        context = {
            'table':table
        }
        return render(request,"update-table.html",context)
    if request.method == "POST":
        table.name = request.POST.get('name')
        table.status = request.POST.get("status") == 'on'
        table.save()
        messages.success(request,"Table is updated successfully!")
        return redirect('/tables/')

@login_required(login_url=settings.LOGIN_URL)
@role_permission_required('app.delete_tablemodel')
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
        "categories": categories,
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

        return redirect('/checkout-success/')
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
    
def CheckoutSuccess(request):
    return render(request, "checkout-success.html")

@login_required(login_url=settings.LOGIN_URL)
@role_permission_required('authentication.add_usermodel')
def CreateUser(request):
    if request.method == "GET":
        roles = RoleModel.objects.all().order_by('-created_at')
        context = {
            'roles': roles,
        }
        return render(request, 'create-user.html', context)
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get("email")
        is_active = request.POST.get('is_active') == 'on'
        is_staff = request.POST.get('is_staff') == 'on'
        is_superuser = request.POST.get('is_superuser') == 'on'
        role_id = request.POST.get('role')
        
        if UserModel.objects.filter(email=email).exists():
            messages.error(request, "Email has already been used!")
            return redirect('/users/')
        
        password = request.POST.get('password')
        password_confirm = request.POST.get('passwordconfirm')
        if password == password_confirm:
            user = UserModel.objects.create_user(
                username=username,
                email=email,
                password=password,
                is_active=is_active,
                is_staff=is_staff,
                is_superuser=is_superuser,
                role_id=role_id
            )
            user.save()
            messages.success(request, "Account was created for " + username)
            return redirect('/users/')
        else:
            messages.error(request, "Password does not match! Please check your password again!")
            return redirect('/users/')

@login_required(login_url=settings.LOGIN_URL)
@role_permission_required('authentication.view_usermodel')
def Users(request):
    users = UserModel.objects.all().order_by('-created_at')
    roles = RoleModel.objects.all().order_by('-created_at')
    context = {
        "users": users,
        "roles": roles
    }
    return render(request, 'users.html',context)

@login_required(login_url=settings.LOGIN_URL)
@role_permission_required('authentication.change_usermodel')
def UpdateUser(request, id):
    user = UserModel.objects.get(id=id)
    if request.method == "GET":
        roles = RoleModel.objects.all().order_by('-created_at')
        context = {
            "user": user,
            "roles": roles
            }
        return render(request, 'update-user.html', context)
    if request.method == 'POST':
        user.email = request.POST.get('email')
        user.username = request.POST.get('username')
        user.is_active = request.POST.get('is_active') == 'on'
        user.is_staff = request.POST.get('is_staff') == 'on'
        user.is_superuser = request.POST.get('is_superuser') == 'on'
        user.role_id = request.POST.get('role')
        if request.POST.get('password'):
            user.set_password(request.POST.get('password'))
        user.save()
        messages.success(request, "User was updated!")
        return redirect('/users/')

@login_required(login_url=settings.LOGIN_URL)
@role_permission_required('authentication.delete_usermodel')
def DeleteUser(request, id):
    user = UserModel.objects.get(id=id)
    user.delete()
    messages.success(request, "User was deleted!")
    return redirect('/users/')

# View to render the main page with a payment list
@login_required(login_url=settings.LOGIN_URL)
@role_permission_required('app.view_sizemodel')
def Sizes(request):
    sizes = SizeModel.objects.all()
    context = {
        'sizes':sizes
    }
    return render(request, 'sizes.html', context)
    
@login_required(login_url=settings.LOGIN_URL)
@role_permission_required('app.add_sizemodel')
def CreateSize(request):
    if request.method == "GET":
        return render(request,"create-size.html")
    if request.method == "POST":
        size = SizeModel.objects.create(
            name = request.POST.get('name')
        )
        size.save()
        messages.success(request,"size is created successfully!")
        return redirect('/sizes/')

@login_required(login_url=settings.LOGIN_URL)
@role_permission_required('app.change_sizemodel')
def UpdateSize(request,id):
    size = SizeModel.objects.get(id = id)
    if request.method == "GET":
        context = {
            'size':size
        }
        return render(request,"update-size.html",context)
    if request.method == "POST":
        size.name = request.POST.get('name')
        size.save()
        messages.success(request,"size is updated successfully!")
        return redirect('/sizes/')

@login_required(login_url=settings.LOGIN_URL)
@role_permission_required('app.delete_sizemodel')
def DeleteSize(request,id):
    size = SizeModel.objects.get(id = id)
    size.delete()
    messages.success(request,"size is deleted successfully!")
    return redirect('/sizes/')

# View to render the main page with a payment list
@login_required(login_url=settings.LOGIN_URL)
@role_permission_required('app.view_meatmodel')
def Meats(request):
    meats = MeatModel.objects.all()
    context = {
        'meats':meats
    }
    return render(request, 'meats.html', context)
    
@login_required(login_url=settings.LOGIN_URL)
@role_permission_required('app.add_meatmodel')
def CreateMeat(request):
    if request.method == "GET":
        return render(request,"create-meat.html")
    if request.method == "POST":
        meat = MeatModel.objects.create(
            name = request.POST.get('name')
        )
        meat.save()
        messages.success(request,"meat is created successfully!")
        return redirect('/meats/')

@login_required(login_url=settings.LOGIN_URL)
@role_permission_required('app.change_meatmodel')
def UpdateMeat(request,id):
    meat = MeatModel.objects.get(id = id)
    if request.method == "GET":
        context = {
            'meat':meat
        }
        return render(request,"update-meat.html",context)
    if request.method == "POST":
        meat.name = request.POST.get('name')
        meat.save()
        messages.success(request,"meat is updated successfully!")
        return redirect('/meats/')

@login_required(login_url=settings.LOGIN_URL)
@role_permission_required('app.delete_meatmodel')
def DeleteMeat(request,id):
    meat = MeatModel.objects.get(id = id)
    meat.delete()
    messages.success(request,"meat is deleted successfully!")
    return redirect('/meats/')

# View to render the main page with a payment list
@login_required(login_url=settings.LOGIN_URL)
@role_permission_required('app.view_spicymodel')
def Spicies(request):
    spicies = SpicyModel.objects.all()
    context = {
        'spicies':spicies
    }
    return render(request, 'spicies.html', context)
    
@login_required(login_url=settings.LOGIN_URL)
@role_permission_required('app.add_spicymodel')
def CreateSpicy(request):
    if request.method == "GET":
        return render(request,"create-spicy.html")
    if request.method == "POST":
        spicy = SpicyModel.objects.create(
            name = request.POST.get('name')
        )
        spicy.save()
        messages.success(request,"spicy is created successfully!")
        return redirect('/spicies/')

@login_required(login_url=settings.LOGIN_URL)
@role_permission_required('app.change_spicymodel')
def UpdateSpicy(request,id):
    spicy = SpicyModel.objects.get(id = id)
    if request.method == "GET":
        context = {
            'spicy':spicy
        }
        return render(request,"update-spicy.html",context)
    if request.method == "POST":
        spicy.name = request.POST.get('name')
        spicy.save()
        messages.success(request,"spicy is updated successfully!")
        return redirect('/spicies/')

@login_required(login_url=settings.LOGIN_URL)
@role_permission_required('app.delete_spicymodel')
def DeleteSpicy(request,id):
    spicy = SpicyModel.objects.get(id = id)
    spicy.delete()
    messages.success(request,"spicy is deleted successfully!")
    return redirect('/spicies/')

def send_websocket_notification(message):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'notifications',
        {
            'type': 'send_notification',
            'message': message,
        }
    )

def OrderConfirm(request, id):
    try:
        table = TableModel.objects.get(id=id)
        cart_items = CartModel.objects.filter(table_id=table.id, status=False)
        total_price = 0
        order_items_details = []

        for item in cart_items:
            total_price += item.product.price * item.quantity
            item.status = True
            item.save()
            order_items_details.append(f"{item.quantity}x {item.product.name} - {item.product.price} each")

        # Create the order and associate it with the table
        order = OrderModel.objects.create(
            table=table,
            total_price=total_price,
        )
        order.save()

        # Add the cart items to the order
        order.cart_items.set(cart_items)
        message = f"Order placed at Table {table.id}: {', '.join(order_items_details)}. Total: {total_price}"

        cart_items_serialized = [{
            'item_id': item.id,
            'quantity': item.quantity,
            'product_name': item.product.name,
            'product_price': item.product.price
        } for item in cart_items]

        message2 = {'id': order.id, 'items': cart_items_serialized, 'table_id': table.id}
       
        send_websocket_notification(message2)

        cart_items.update(status=True)

        return redirect(f"/carts/{table.id}/")
    except Exception as e:
        print(e)
        return redirect('/')


def Kitchen(request):
    return render(request,'kitchen.html')