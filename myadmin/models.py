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
    number = models.BigIntegerField(default=0,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)