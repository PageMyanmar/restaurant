from django.contrib import admin
from myadmin.models import *
from user.models import *
from authentication.models import *
# Register your models here.

admin.site.register(UserModel)
admin.site.register(CategoryModel)
admin.site.register(ProductModel)
admin.site.register(CartModel)
admin.site.register(TableModel)