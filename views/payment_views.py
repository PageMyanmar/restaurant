from django.http import JsonResponse
from django.shortcuts import redirect,render
from app.models import *
from app.models import *
import json
from django.contrib import messages

# View to render the main page with a payment list
def Payments(request):
    payments = PaymentModel.objects.all()
    context = {
        'payments':payments
    }
    return render(request, 'payments.html', context)
    
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

def DeletePayment(request,id):
    payment = PaymentModel.objects.get(id = id)
    payment.delete()
    messages.success(request,"payment is deleted successfully!")
    return redirect('/payments/')
    