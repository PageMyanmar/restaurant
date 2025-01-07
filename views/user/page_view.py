from django.shortcuts import render
from myadmin.models import *
from user.models import *
from django.http import JsonResponse
from django.utils.dateformat import format as format_date

def Index(request):
    categories = CategoryModel.objects.all().order_by('-created_at')
    products = ProductModel.objects.all().order_by("-created_at")
    
    context = {
        'categories': categories,
        'products': products,
    }
    return render(request, 'user/index.html',context)

def ProductsByCategory(request,id,t_id):
    category = CategoryModel.objects.get(id = id)
    table = TableModel.objects.get(id = t_id)
    products = ProductModel.objects.filter(category = category).order_by("-created_at")
    
    context = {
        'products': products,
        'category': category,
        'table': table,
    }
    return render(request, 'user/products-by-category.html',context)

def Products(request):
    products = ProductModel.objects.all().order_by("-created_at") 

    context = {
        'products': products
        }
    return render(request, 'user/shop.html',context)

def ProductDetails(request, id):
    product = ProductModel.objects.get(id=id)

    # Fetch related products based on the same category
    reviews = ReviewModel.objects.filter(product = product).order_by('-created_at')

    context = {
        'product': product,
        'reviews': reviews,
        'range': range(1, 6),  # Provide the range for the star ratings
    }
    return render(request, 'user/product-details.html', context)

def GetCounts(request):
    # Assuming the table ID is stored in the session or passed as a query parameter
    table_id = request.GET.get('table_id')  # Example: table_id stored in the session
    if not table_id:
        table_id = request.GET.get('table_id')  # Fallback to query parameter

    if table_id:
        table = TableModel.objects.filter(id=table_id).first()
        if table:
            cart_count = CartModel.objects.filter(table=table).count()
            return JsonResponse({'cart_count': cart_count})
    return JsonResponse({'cart_count': 0})  # Default to 0 if no table or items are foided

def MyAccount(request):
    if request.user.is_authenticated:
        user = request.user
        context = {
            'user': user
            }
        return render(request, 'user/my-account.html', context)

def SubmitReview(request):
    if request.method == 'POST':

        product_id = request.POST.get('product_id')
        try:
            product = ProductModel.objects.get(id=product_id)
        except ProductModel.DoesNotExist:
            return JsonResponse({'error': 'Product not found!'}, status=404)

        name = request.POST.get('name')
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        # Required Fields Validation
        if not (name and  comment):
            return JsonResponse({'error': 'Name and Comment fields are required!'}, status=400)

        # Default Rating Validation
        try:
            rating = int(rating) if rating else 0
        except ValueError:
            rating = 0

        # Create and Save Review
        review = ReviewModel.objects.create(
            product=product,
            name=name,
            rating=rating,
            comment=comment,
        )
        review.save()

        # Return JSON Response with Updated Review Count
        return JsonResponse({
            'message': 'Review submitted successfully!',
            'name': review.name,
            'comment': review.comment,
            'rating': review.rating,
            'created_at': format_date(review.created_at, "F j, Y, g:i a"),
        }, status=200)

    return JsonResponse({'error': 'Invalid request method'}, status=400)

def Contact(request):
    if request.method == "GET":
        return render(request, 'user/contact.html')
    if request.method == 'POST':
        # Extract form data
        name = request.POST.get('name')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Validate required fields
        if not (subject and message):
            return JsonResponse({'error': 'Your name, subject and message fields are required!'}, status=400)

        # Save the contact form entry
        contact = ContactModel.objects.create(
            name = name,
            subject=subject,
            message=message
        )
        contact.save()

        return JsonResponse({'message': 'Your message has been sent successfully!'}, status=200)

    return JsonResponse({'error': 'Invalid request method'}, status=400)