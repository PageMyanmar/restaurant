from django.db import models
from authentication.models import *

# Create your models here.

class TableModel(models.Model):
    name = models.CharField(max_length=200)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class CategoryModel(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='category/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class ProductModel(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='product/')
    price = models.IntegerField(default=0,null=True,blank=True)
    quantity = models.IntegerField(default=0, verbose_name="Current Stock")
    category = models.ForeignKey(CategoryModel,on_delete=models.SET_NULL,null=True,default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class PaymentModel(models.Model):
    name = models.CharField(max_length=200)
    number = models.CharField(max_length=200,default=None,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CartModel(models.Model):
    table = models.ForeignKey(TableModel,on_delete=models.SET_NULL,null=True)
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, null=True)
    total_price = models.BigIntegerField(default=0, null=True)
    note = models.TextField(null=True,blank=True,default=None)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class OrderModel(models.Model):
    table = models.ForeignKey(TableModel, on_delete=models.SET_NULL, null=True)
    cart_items = models.ManyToManyField(CartModel)
    total_price = models.BigIntegerField(default=0, null=True)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CheckoutModel(models.Model):
    table = models.ForeignKey(TableModel,on_delete=models.SET_NULL,default=None,null=True)
    payment = models.ForeignKey(PaymentModel,on_delete=models.CASCADE,default=None,null=True,blank=True)
    cart_items = models.ManyToManyField(CartModel, related_name='cart_items')
    total = models.BigIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ReviewModel(models.Model):
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=255)
    email = models.EmailField()
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Review by {self.name} for {self.product.name}'
    
class ContactModel(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20,default=None)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)