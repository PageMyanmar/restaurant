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
from views import auth_views,cart_views,category_views,page_views,payment_views,product_views,role_views,table_views,user_views

urlpatterns = [
    path("abcde/", admin.site.urls),
    # re_path(r'^.*/$', Error404),

    # ==================== USER URLS ====================
    path('',page_views.Index),
    path('trncs/',auth_views.Login),
    path('register/',auth_views.Register),
    path('logout/',auth_views.Logout),
    path('subscribe/',auth_views.Subscribe),
    path('get-counts/', page_views.GetCounts),
    path('my-account/',page_views.MyAccount),
    path('submit-review/',page_views.SubmitReview),
    path('shop/',page_views.Products),
    path('contact/',page_views.Contact),
    path('category/<int:id>/products/<int:t_id>/',page_views.ProductsByCategory),

    # Cart
    path('carts/<int:id>/',cart_views.Carts),
    path('add-to-cart/<int:p_id>/<int:t_id>/', cart_views.AddToCart),
    path('remove-from-cart/<int:id>/', cart_views.RemoveFromCart),
    path('update-cart/<int:id>/', cart_views.UpdateCart),

    # Products
    path('products/details/<int:id>/',page_views.ProductDetails),

    # ==================== ADMIN URLS ====================

    # Roles
    path('roles/',role_views.Roles),
    path('create-role/',role_views.CreateRole),
    path('update-role/<int:id>/',role_views.UpdateRole),
    path('delete-role/<int:id>/',role_views.DeleteRole),

    # Invoices
    path('invoices/',page_views.Invoices),

    # Users
    path('users/',user_views.Users),
    path('create-user/',user_views.CreateUser),
    path('update-user/<uuid:id>/',user_views.UpdateUser),
    path('delete-user/<uuid:id>/',user_views.DeleteUser),

    # Categories
    path('categories/',category_views.Categories),
    path('create-category/',category_views.CreateCategory),
    path('update-category/<int:id>/',category_views.UpdateCategory),
    path('delete-category/<int:id>/',category_views.DeleteCategory),

    # Products
    path('products/',product_views.Products),
    path('create-product/',product_views.CreateProduct),
    path('update-product/<int:id>/',product_views.UpdateProduct),
    path('delete-product/<int:id>/',product_views.DeleteProduct),

    # Tables
    path('tables/',table_views.Tables),
    path('create-table/',table_views.CreateTable),
    path('update-table/<int:id>/',table_views.UpdateTable),
    path('delete-table/<int:id>/',table_views.DeleteTable),
    path('order/<int:id>/',table_views.Order),
    path('order-confirm/<int:id>/',cart_views.OrderConfirm),
    path('checkout/<int:id>/',table_views.Checkout),

    #Payment
    path('payments/',payment_views.Payments),
    path('create-payment/',payment_views.CreatePayment),
    path('update-payment/<int:id>/',payment_views.UpdatePayment),
    path('delete-payment/<int:id>/',payment_views.DeletePayment)

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)