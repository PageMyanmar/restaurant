"""
URL configuration for restaurant project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from app.views import *
urlpatterns = [
    path("abcde/", admin.site.urls),
    # re_path(r'^.*/$', Error404),

    # ==================== USER URLS ====================
    path('',Index),
    path('trncs/',Login),
    path('register/',Register),
    path('logout/',Logout),
    path('shop/',Products),
    path('contact/',Contact),
    path('category/<int:id>/products/<int:t_id>/',ProductsByCategory),

    # Cart
    path('carts/<int:id>/',Carts),
    path('add-to-cart/<int:p_id>/<int:t_id>/', AddToCart),
    path('remove-from-cart/<int:id>/', RemoveFromCart),
    path('update-cart/<int:id>/', UpdateCart),

    # ==================== ADMIN URLS ====================

    # Roles
    path('roles/',Roles),
    path('create-role/',CreateRole),
    path('update-role/<int:id>/',UpdateRole),
    path('delete-role/<int:id>/',DeleteRole),

    # Invoices
    path('invoices/',Invoices),

    # Users
    path('users/',Users),
    path('create-user/',CreateUser),
    path('update-user/<uuid:id>/',UpdateUser),
    path('delete-user/<uuid:id>/',DeleteUser),

    # Categories
    path('categories/',Categories),
    path('create-category/',CreateCategory),
    path('update-category/<int:id>/',UpdateCategory),
    path('delete-category/<int:id>/',DeleteCategory),

    # Products
    path('products/',Products),
    path('create-product/',CreateProduct),
    path('update-product/<int:id>/',UpdateProduct),
    path('delete-product/<int:id>/',DeleteProduct),

    # Tables
    path('tables/',Tables),
    path('create-table/',CreateTable),
    path('update-table/<int:id>/',UpdateTable),
    path('delete-table/<int:id>/',DeleteTable),
    path('order/<int:id>/',Order),
    path('order-confirm/<int:id>/',OrderConfirm),
    path('checkout/<int:id>/',Checkout),

    #Payment
    path('payments/',Payments),
    path('create-payment/',CreatePayment),
    path('update-payment/<int:id>/',UpdatePayment),
    path('delete-payment/<int:id>/',DeletePayment)

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)