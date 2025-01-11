from django.shortcuts import redirect,render
from app.models import *
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required
from app.decorators import role_permission_required

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
    