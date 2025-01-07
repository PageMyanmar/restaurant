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
from django.urls import path,re_path,include
from django.conf.urls.static import static
from django.conf import settings
from views.user import auth_view,page_view,cart_view
from views.admin import auth_views,role_views,page_views,user_views,category_views,product_views,table_views,payment_views

urlpatterns = [
    path("abcde/", admin.site.urls),
    # re_path(r'^.*/$', Error404),

    # ==================== USER URLS ====================
    path('',page_view.Index),
    path('trncs/',auth_view.Login),
    path('register/',auth_view.Register),
    path('logout/',auth_view.Logout),
    path('subscribe/',auth_view.Subscribe),
    path('get-counts/', page_view.GetCounts),
    path('my-account/',page_view.MyAccount),
    path('submit-review/',page_view.SubmitReview),
    path('shop/',page_view.Products),
    path('contact/',page_view.Contact),
    path('category/<int:id>/products/<int:t_id>/',page_view.ProductsByCategory),
    path('update-profile/',auth_view.UpdateProfile),
    path('change-password/',auth_view.ChangePassword),

    # Cart
    path('carts/<int:id>/',cart_view.Carts),
    path('add-to-cart/<int:p_id>/<int:t_id>/', cart_view.AddToCart),
    path('remove-from-cart/<int:id>/', cart_view.RemoveFromCart),

    # Products
    path('products/details/<int:id>/',page_view.ProductDetails),

    # ==================== ADMIN URLS ====================
    path('khaing/',auth_views.AdminLogin),
    path('dashboard/',page_views.Dashboard),
    path('admin_logout/',auth_views.AdminLogout),

    # Roles
    path('roles/',role_views.Roles),
    path('roles/create/',role_views.RoleCreate),
    path('roles/update/<int:id>/',role_views.RoleUpdate),
    path('roles/delete/<int:id>/',role_views.RoleDelete),

    # Users
    path('users/',user_views.Users),
    path('users/create/',user_views.UserCreate),
    path('users/update/<uuid:id>/',user_views.UserUpdate),
    path('users/delete/<uuid:id>/',user_views.UserDelete),

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
    path('order-confirm/<int:id>/',cart_view.OrderConfirm),

    #Payment
    path('payments/',payment_views.Payments),
    path('create-payment/',payment_views.CreatePayment),
    path('update-payment/<int:id>/',payment_views.UpdatePayment),
    path('delete-payment/<int:id>/',payment_views.DeletePayment)

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)