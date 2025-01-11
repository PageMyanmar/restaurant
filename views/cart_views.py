from app.models import CartModel, ProductModel,OrderModel
from app.models import TableModel
from django.shortcuts import render,redirect
from django.contrib import messages
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

def send_websocket_notification(message):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'notifications',
        {
            'type': 'send_notification',
            'message': message,
        }
    )

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

        if product.quantity < int(quantity):
            messages.error(request, 'Quantity is not available')
            return redirect(f"/order/{table.id}/")
        
        table.status = True
        table.save()

        product.quantity -= quantity
        product.save()

        cart = CartModel.objects.create(
            table_id=table.id,
            product_id=product.id,
            quantity=quantity,
            note=request.POST.get('note'),
        )
        cart.save()
        messages.success(request, f'({cart.quantity}) {cart.product.name} are added to cart successfully! {cart.note}')
        return redirect(f"/order/{table.id}/")  # Redirect back to the order page

def UpdateCart(request,id):
    cart = CartModel.objects.get(id = id)
    if request.method == 'POST':
        cart.quantity = int(request.POST.get('quantity'))
        cart.note = request.POST.get('note')
        cart.save()
        messages.success(request, f'Cart updated successfully!')
        return redirect(f"/carts/{cart.table.id}/")  # Redirect back to the order pag

def RemoveFromCart(request,id):
    cart = CartModel.objects.get(id=id)
    product = cart.product
    product.quantity += cart.quantity
    product.save()
    table = cart.table
    cart.delete()
    messages.success(request, f'{cart.product.name} is removed from cart successfully!')
    return redirect(f'/carts/{table.id}/')

def OrderConfirm(request, id):
    table = TableModel.objects.get(id=id)
    cart_items = CartModel.objects.filter(table=table, status=False)
    total_price = 0
    for item in cart_items:
        total_price += item.product.price * item.quantity
        item.status = True
        item.save()
    
    # Create the order and associate it with the table
    order = OrderModel.objects.create(
        table=table,
        total_price=total_price,
    )
    order.save()

    # Add the cart items to the order (no need to add the 'order' field in CartModel)
    order.cart_items.set(cart_items)

    # Mark all cart items as confirmed (status=True)
    cart_items.update(status=True)

    # Send success message
    # Trigger a success message with cart item quantity
    message = f"စားပွဲနံပါတ် {table.id} မှ order မှာယူထားပါသည်။"
    messages.success(request, message)   
    # Send WebSocket notification
    send_websocket_notification(message)
    return redirect(f"/carts/{table.id}/")